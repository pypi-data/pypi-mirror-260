
import os

import pandas as pd
import pandas_ta as ta
import yfinance as yf

from datetime import time, date, datetime, timedelta
from pytz import timezone

import pymannkendall as mk
import math
import numpy as np

from option_trader.consts import asset as at

from option_trader.utils.data_getter import get_price_history, get_price
from option_trader.utils.data_getter import get_next_earning_date
from option_trader.utils.data_getter import get_support_resistence_levels
from option_trader.utils.data_getter import get_option_exp_date
from option_trader.utils.data_getter import get_option_leg_details
from option_trader.utils.data_getter import get_option_leg_IV_delta
from option_trader.utils.data_getter import afterHours


from option_trader.backtest.stock.bollingerBands import BB_strategy, plot_BB
from option_trader.backtest.stock.macd import MACD_strategy, plot_MACD
from option_trader.backtest.stock.mfi import MFI_strategy, plot_MFI
from option_trader.backtest.stock.rsi import RSI_strategy, plot_RSI

from option_trader.utils.predictor  import predict_price_range
from option_trader.entity import quote
from option_trader.consts import asset           

from option_trader.settings.ta_strategy import CustomStrategy
from  option_trader.settings import app_settings
import logging
import warnings
warnings.filterwarnings( "ignore", module = "matplotlib\..*" )


import os
import sqlite3


class cname():
    symbol                  = 'symbol'
    last_update_time        = 'last_update_time'
    forward_PE              = 'forward_PE'    
    rating                  = 'rating'   
    earning                 = 'earning'
    target_low              = 'target_low'
    target_high             = 'target_high'
    last_quote              = 'last_quote'
    day_range               = 'day_range'
    avg_price_ratio         = 'avg_price_ratio'
    avg_volume_ratio        = 'avg_volume_ratio'                        
    support                 = 'support'
    resistence              = 'resistence'
    ten_days_gain           = 'ten_days_gain'    
    ten_days_high           = 'ten_days_high'
    ten_days_low            = 'ten_days_low'
    HV                      = 'HV'
    exp_1_IV                = 'exp_1_IV'
    exp_1_IV_HV_dif         = 'exp_1_IV_HV_dif'
    exp_1_delta             = 'exp_1_delta'

    exp_2_IV                = 'exp_2_IV'
    exp_2_IV_HV_dif         = 'exp_2_IV_HV_dif'
    exp_2_delta             = 'exp_2_delta'

    exp_3_IV                = 'exp_3_IV'
    exp_3_IV_HV_dif         = 'exp_3_IV_HV_dif'
    exp_3_delta             = 'exp_3_delta'

    exp_4_IV                = 'exp_4_IV'
    exp_4_IV_HV_dif         = 'exp_4_IV_HV_dif'
    exp_4_delta             = 'exp_4_delta'
       
    trend                   = 'trend'
    slope                   = 'slope'
    BBand                   = 'BBand'
    RSI                     = 'RSI'
    MFI                     = 'MFI'
    MACD                    = 'MACD'

monitor_schema =  cname.symbol                + " TEXT,"+\
                  cname.last_update_time      + " TEXT,"+\
                  cname.forward_PE            + " REAL,"+\
                  cname.rating                + " REAL,"+\
                  cname.earning               + " TEXT,"+\
                  cname.target_low            + " REAL,"+\
                  cname.target_high           + " REAL,"+\
                  cname.last_quote            + " REAL,"+\
                  cname.day_range             + " REAL,"+\
                  cname.avg_price_ratio       + " REAL,"+\
                  cname.avg_volume_ratio      + " REAL,"+\
                  cname.ten_days_gain         + " REAL,"+\
                  cname.ten_days_high         + " REAL,"+\
                  cname.ten_days_low          + " REAL,"+\
                  cname.HV                    + " REAL,"+\
                  cname.exp_1_IV_HV_dif       + " REAL,"+\
                  cname.exp_1_IV              + " REAL,"+\
                  cname.exp_1_delta           + " REAL,"+\
                  cname.exp_2_IV_HV_dif       + " REAL,"+\
                  cname.exp_2_IV              + " REAL,"+\
                  cname.exp_2_delta           + " REAL,"+\
                  cname.exp_3_IV_HV_dif       + " REAL,"+\
                  cname.exp_3_IV              + " REAL,"+\
                  cname.exp_3_delta           + " REAL,"+\
                  cname.exp_4_IV_HV_dif       + " REAL,"+\
                  cname.exp_4_IV              + " REAL,"+\
                  cname.exp_4_delta           + " REAL,"+\
                  cname.support               + " REAL,"+\
                  cname.resistence            + " REAL,"+\
                  cname.trend                 + " TEXT,"+\
                  cname.slope                 + " REAL,"+\
                  cname.BBand                 + " REAL,"+\
                  cname.MFI                   + " REAL,"+\
                  cname.RSI                   + " REAL,"+\
                  cname.MACD                  + " REAL,"+\
                  "PRIMARY KEY ("+cname.symbol+")"

class monitor_mgr():

    def __init__(self, this_site):
        self.this_site = this_site 
        self.logger = logging.getLogger(__name__)

        self.db_path = os.path.join(self.this_site.site_root, 'monior.db')                                                  
        if os.path.exists(self.db_path ) == False:
            self.db_conn = sqlite3.connect(self.db_path)      
            cursor = self.db_conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS monitor_table ("+monitor_schema+")")   
            self.db_conn.commit()                                             
        else:
            self.db_conn = sqlite3.connect(self.db_path)   

    def write_to_db(self, df):

        members = [attr for attr in dir(cname) if not \
                    callable(getattr(cname, attr)) and not attr.startswith("__")]                                
        #members.sort()
        field_names = str(members).strip("[]")           
        values = '?' + ",?" * (len(members)-1)
        fields = []
        for fld in members:
            fields.append(df[fld])
        sql = "INSERT OR REPLACE INTO monitor_table ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        self.db_conn.commit()  

    def expand_monitor_list(self, asset_list):
        monitor_list = self.get_monitor_list()

        if app_settings.DATABASES == 'sqlite3':                 
            filter=[]               
            for symbol in asset_list:
                if symbol in monitor_list:
                    continue                                                        
                sql = "INSERT INTO monitor_table ("+asset.SYMBOL+") VALUES (?)"              
                try:
                    cursor = self.db_conn.cursor()
                    cursor.execute(sql, [symbol])
                except Exception as e:                    
                    self.logger.warning('Add %s failed %s' % (symbol, str(e)))
                    continue
                filter.append(symbol)                
        else:
            self.logger.error("sqlite3 only for now %s")

        if len(filter) > 0:
            self.db_conn.commit()            
            self.refresh_monitor_list(filter=filter)

    def get_monitor_list(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                cursor = self.db_conn.cursor()                    
                symbols = [symbol[0] for symbol in cursor.execute("SELECT "+asset.SYMBOL+ " FROM monitor_table")]
                return symbols
            except Exception as e:
                self.logger.exception(e)   
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_monitor_df(self, filter=[]):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                import pandas as pd                
                df = pd.read_sql_query("SELECT * FROM monitor_table", self.db_conn)                           
                df = df[df[asset.SYMBOL].isin(filter)] if len(filter)>0 else df    
                today = datetime.now(timezone(app_settings.TIMEZONE))                
                for i, r in df.iterrows():
                    price_history = get_price_history(r.symbol, period='1mo')
                    q = yf.Ticker(r.symbol).get_info()                       
                    df.at[i, 'quote'] = round(price_history['Close'][-1],2)                    
                    df.at[i, 'day high'] = round(price_history['High'][-1],2)
                    df.at[i, 'day low'] = round(price_history['Low'][-1],2)
                    df.at[i, 'day change'] = round(df.at[i, 'quote'] - price_history['Close'][-2],2)                   
                    df.at[i, 'day change%'] = round((df.at[i, 'quote'] - price_history['Close'][-2])/price_history['Close'][-2],2) * 100     
                    df.at[i, 'day range%'] = round((df.at[i, 'quote'] - df.at[i, 'day low'])/(df.at[i, 'day high'] - df.at[i, 'day low']),2) * 100     
                    df.at[i, 'volumn%'] = 100 * round(price_history['Volume'][-1]/q['averageVolume'],2)
                    df.at[i, '10D change%'] = round((df.at[i, 'quote'] - price_history['Close'][-10])/price_history['Close'][-10],2) * 100     

                    try:
                        earning_date = r[cname.earning]
                        ##datetime.fromisoformat(earning_date)
                        earning_date = pd.Timestamp(earning_date).tz_localize(timezone(app_settings.TIMEZONE))                 
                        days_to_earning = (earning_date - today).days+1               
                    except Exception as e:
                        days_to_earning = np.nan
                                    
                    df.at[i, 'days to earning'] =  days_to_earning 

                return df
            except Exception as e:
                self.logger.exception(e)   
                return pd.DataFrame()
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_monitor_rec(self, symbol):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                import pandas as pd                
                df = pd.read_sql_query("SELECT * FROM monitor_table WHERE symbol ='" + symbol + "'", self.db_conn)  
                if df.shape[0] > 0:
                    return df.to_dict('records')[0]
                
                self.expand_monitor_list([symbol])
                df = pd.read_sql_query("SELECT * FROM monitor_table WHERE symbol ='" + symbol + "'", self.db_conn)  
                return df.to_dict('records')[0]                                 
            except Exception as e:
                self.logger.exception(e) 
                return {}  
        else:
            self.logger.error("sqlite3 only for now %s")

    def refresh_monitor_list(self, filter=[], check_afterhour=True):
        
        df = self.get_monitor_df()

        for i, r in df.iterrows(): 

            if len(filter) > 0 and r[cname.symbol] not in filter:
                continue                       

            if len(filter) > 0:
                refresh_ta = True
            elif df.at[i, cname.last_update_time] != None:
                
                from dateutil import parser
                from dateutil import tz 

                date_string = df.at[i, cname.last_update_time]
                x = timezone(app_settings.TIMEZONE)                
                tzinfos = {"EST": tz.gettz("America/New_York")}
                last_update_time = parser.parse(date_string,tzinfos=tzinfos)
                current = datetime.now(timezone(app_settings.TIMEZONE))
                minutes_diff = (current - last_update_time).total_seconds() / 60.0    

                if afterHours():
                    if minutes_diff < 60 * 24:
                        continue
        
                if minutes_diff < 60:
                    continue
                
                refresh_ta = True if minutes_diff > 60 * 24 else False 
            else:
                refresh_ta = True

            try: 
                self.refresh_asset_info(i, df, refresh_ta=refresh_ta, check_afterhour=check_afterhour)         

                self.write_to_db(df.to_dict('records')[i])

            except Exception as ex:
                self.logger.exception(ex)
                pass 

        return df

    def refresh_asset_info(self, i, df, refresh_ta=True, check_afterhour=True):

        symbol = df.at[i,cname.symbol]
        data = get_price_history(symbol, period='1y')
        if data.shape[0] <= 15:
            self.logger.error('Cannot get history for %s' % symbol)
            return 
        self.refresh_asset_basic_info(i, df, data, check_afterhour)   
        if refresh_ta:
            data.ta.cores = 2
            customStrateg = ta.Strategy(
                name="Option Trader",
                description="BBANDS, RSI, MACD, MFI, TREND",
                ta=[
                    {"kind": "rsi"},
                    {"kind": "macd", "fast": 12, "slow": 26},
                    {"kind": "bbands", "length": 20},          
                    {"kind": "mfi", "period": 14}     
                ]
            )

            data.ta.strategy(customStrateg)
            if "BBL_20_2.0" not in data.columns:
                self.logger.error('data ta failed for %s' % symbol)    
                return
            data.dropna(subset=["BBL_20_2.0"])    

            self.refresh_BB(i, df, data)
            self.refresh_RSI(i, df, data)        
            self.refresh_MFI(i, df, data)        
            self.refresh_MACD(i, df, data)        

        df.at[i, cname.last_update_time] = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")
        
        self.logger.info('Refresh %s' % symbol)   
        #logger.debug('%s refreshed' %symbol)
        
    def refresh_asset_basic_info(self, i, df, price_history, check_afterhour=True):        

        from option_trader.utils.data_getter import afterHours

        logger = logging.getLogger(__name__)
        
        symbol = df.at[i, cname.symbol]        

        df.at[i, cname.last_update_time] = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")

        last_price = price_history['Close'][-1]

        try:
            q = yf.Ticker(symbol).get_info()   
            if afterHours():
                day_high =  q['regularMarketDayHigh']
                day_low  =  q['regularMarketDayLow']         
                volume = q['regularMarketVolume']        
            else:
                day_high =  q['dayHigh']
                day_low  =  q['dayLow'] 
                volume = q['volume']    

            fifty_two_weeks_low =  q['fiftyTwoWeekLow']
            fifty_two_weeks_high = q['fiftyTwoWeekHigh']
            fifty_two_weeks_range_pos = ((last_price - fifty_two_weeks_low)/(fifty_two_weeks_high-fifty_two_weeks_low))*100 

            avg_volume = float(q['averageVolume'])

            volume_range_pos = (volume/avg_volume)*100   if avg_volume > 0 else np.nan         
        
            df.at[i, cname.forward_PE] = round(q['forwardPE'],2) if 'forwardPE' in q else np.nan       

            df.at[i, cname.rating] = float(q['recommendationMean']) if 'recommendationMean' in q else 0

        except Exception as ex:
            #logger.exception(ex)
            day_high =  price_history['High'][-1]
            day_low  =  price_history['Low'][-1] 
            volume = float(price_history['Volume'][-1])           

            fifty_two_weeks_low =  price_history['Close'].min()
            fifty_two_weeks_high = price_history['Close'].max()
            fifty_two_weeks_range_pos = ((last_price - fifty_two_weeks_low)/(fifty_two_weeks_high-fifty_two_weeks_low))*100
            avg_volume = price_history['Volume'].mean()
            volume_range_pos = (volume/avg_volume)*100  if avg_volume > 0 else np.nan         
            #df.at[i, 'forward_PE'] =  np.nan 

        day_range_pos = ((last_price - day_low)/(day_high-day_low)) * 100
            
        report_date = get_next_earning_date(symbol)        

        df.at[i, cname.earning] = '' if report_date == None else report_date.strftime('%m-%d-%Y')  
        #df.at[i, 'days to earning']  =np.nan if report_date == None else (report_date - today).days 

        ed = get_option_exp_date(symbol, min_days_to_expire=app_settings.MIN_DAYS_TO_EXPIRE, max_days_to_expire=app_settings.MAX_DAYS_TO_EXPIRE)
        if len(ed) == 0:
            return
        
        target_date_list = [ed[0]]

        target_date_list = [get_option_exp_date(symbol, min_days_to_expire=app_settings.STOCK_RANGE_PREDICT_DAYS, max_days_to_expire=np.nan)[0]]
        predictlist = predict_price_range(symbol, target_date_list=target_date_list)
        exp_date_list = predictlist['exp_date_list']
        if len(exp_date_list) > 0:
            df.at[i, cname.target_low] = round(predictlist[exp_date_list[0]][quote.LOW],2)      
            df.at[i, cname.target_high] = round(predictlist[exp_date_list[0]][quote.HIGH],2)  
                        
        df.at[i, cname.last_quote] = round(last_price,2)       
        df.at[i, cname.day_range] =  round(day_range_pos,2)
        df.at[i, cname.avg_price_ratio] = round(fifty_two_weeks_range_pos,2)
        df.at[i, cname.avg_volume_ratio] = round(volume_range_pos,2)                      
        support, resistence = get_support_resistence_levels(symbol, price_history)
        df.at[i, cname.support] = round(support,2) if support != None else np.nan
        df.at[i, cname.resistence] = round(resistence,2) if resistence != None else np.nan                    

        df.at[i, cname.ten_days_gain] = round((((last_price-price_history['Close'][-11])/last_price)*100),2)
        df.at[i, cname.ten_days_high] = round(price_history['High'].rolling(window=10).max().shift(1)[-1],2)
        df.at[i, cname.ten_days_low] = round(price_history['Low'].rolling(window=10).min().shift(1)[-1],2)   

        TRADING_DAYS =252
        returns = np.log(price_history['Close']/price_history['Close'].shift(1))
        returns.fillna(0, inplace=True)
        volatility = returns.rolling(window=20).std()*np.sqrt(TRADING_DAYS)
        hv = round(volatility[-1],2)    

        df.at[i, 'HV'] = hv #"{:.2f}".format(hv*100)

        def get_iv_list(symbol, data, count):     
            exp_tbl = get_option_exp_date(symbol)               
            iv = []
            delta=[]
            
            for exp_date in exp_tbl:    
                eiv, edelta = get_option_leg_IV_delta(symbol, exp_date, at.CALL)           
                iv.append(eiv)
                delta.append(edelta)
                count -= 1
                if count == 0:
                    return iv, delta            
            return iv, delta 

        if check_afterhour and afterHours() == False: # After option qiote not avaialbe

            iv, delta = get_iv_list(symbol, price_history, 4)
                
            if len(iv) > 0:        
                df.at[i, cname.exp_1_IV]  = round(iv[0],3) # "{:.2f}".format(iv[0]*100)
                df.at[i, cname.exp_1_IV_HV_dif]  = round(100 * ((df.at[i, cname.exp_1_IV]-df.at[i, cname.HV])/df.at[i, cname.HV]),2)        
                df.at[i, cname.exp_1_delta] = round(delta[0],3) #"{:.2f}".format(delta[0])    
            if len(iv) > 1:            
                df.at[i, cname.exp_2_IV]  = round(iv[1],3) #"{:.2f}".format(iv[1]*100)
                df.at[i, cname.exp_2_IV_HV_dif]  = round(100 * ((df.at[i, cname.exp_2_IV]-df.at[i, cname.HV])/df.at[i, cname.HV]),2)           
                df.at[i, cname.exp_2_delta] = round(delta[1],3) #"{:.2f}".format(delta[1])
            if len(iv) > 2:                  
                df.at[i, cname.exp_3_IV]  =  round(iv[2],3) #"{:.2f}".format(iv[2]*100)
                df.at[i, cname.exp_3_IV_HV_dif]  = round(100 * ((df.at[i, cname.exp_3_IV]-df.at[i, cname.HV])/df.at[i, cname.HV]),2)             
                df.at[i, cname.exp_3_delta] = round(delta[2],3) #"{:.2f}".format(delta[2])
            if len(iv) > 3:
                df.at[i, cname.exp_4_IV]  =  round(iv[3],3) #"{:.2f}".format(iv[3]*100)       
                df.at[i, cname.exp_4_IV_HV_dif]  = round(100 * ((df.at[i, cname.exp_4_IV]-df.at[i, cname.HV])/df.at[i, cname.HV]),2)             
                df.at[i, cname.exp_4_delta] = round(delta[2],3) #"{:.2f}".format(delta[3])
                                            
    def refresh_BB(self, i, df, data):            
        bb_pos = data['BBP_20_2.0'][-1]        
        last_action, last_action_price, recent, total_profit = BB_strategy(data,app_settings.TREND_WINDOW_SIZE)  
        #BB_display = last_action + " {:.2f}".format(last_action_price) if (last_action != '' and recent) else "{:.2f}".format(bb_pos)                  
        BB_display = "{:.2f}".format(bb_pos)                  
        address = plot_BB(df.at[i, cname.symbol], data)
        df.at[i, cname.BBand] =  round(bb_pos,2) # BB_display
        df.at[i, 'bb_link'] = address 
        s = app_settings.TREND_WINDOW_SIZE
        gfg_data = [0] * s
        # perform Mann-Kendall Trend Test   
        last_date_index = len(data.index)-1        
        for j in range(s):        
            gfg_data[j] = data['BBM_20_2.0'][last_date_index-s+1+j]    
        x = mk.original_test(gfg_data)            

        df.at[i, cname.trend] = x.trend
        df.at[i, cname.slope] = round(x.slope,2)    

    def refresh_RSI(self, i, df, data):     
        last_action, last_action_price, recent, total_profit = RSI_strategy(data)          
        rsi = data['RSI_14'][-1]
        #RSI_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else "{:.2f}".format(rsi)      
        RSI_display = "{:.2f}".format(rsi)      
        address =  plot_RSI(df.at[i, cname.symbol], data)                 
        df.at[i, cname.RSI] =  round(rsi,2) #RSI_display
        df.at[i, 'rsi_link'] = address                  

    def refresh_MFI(self, i, df, data):           
        last_action, last_action_price, recent, total_profit = MFI_strategy(data)  
        mfi = data['MFI_14'][-1]
        address =  plot_MFI(df.at[i, cname.symbol], data) 
        #MFI_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else "{:.2f}".format(mfi)          
        MFI_display = "{:.2f}".format(mfi)          
        df.at[i, cname.MFI] =  round(mfi,2) #MFI_display
        df.at[i, 'mfi_link'] = address    
        
    def refresh_MACD(self, i, df, data):                
        last_action, last_action_price, recent, total_profit = MACD_strategy(data)  
        macd = data['MACD_12_26_9'][-1]
        address = plot_MACD(df.at[i, cname.symbol], data)
        #MACD_display = last_action + " {:.2f}".format(last_action_price) if (recent and last_action != '') else"{:.2f}".format(macd)          
        MACD_display = "{:.2f}".format(macd)          
        df.at[i, cname.MACD] =  round(macd,2)#MACD_display
        df.at[i, 'macd_link'] = address                             


if __name__ == '__main__':

    import sys

    sys.path.append(r'\\Users\\jimhu\\option_trader\src')
    
    from option_trader.admin.site import site

    site_name = 'mysite'

    mysite = site(site_name)

    mysite.expand_monitor_list(['SMCI'])

    #mysite.refresh_site_monitor_list()