

from option_trader.consts   import strategy as st
from option_trader.tools.trade_factory   import get_watchlist_trade_targets 
#from option_trader.settings.trade_config import entryCrit, riskManager, runtimeConfig, marketCondition

from option_trader.entity.position_summary import position_summary_col_name as pscl
from option_trader.entity.position         import position_col_name as pcl
from option_trader.entity import quote
from datetime import datetime
from pytz import timezone

from option_trader.utils.predictor import predict_price_range
from option_trader.utils.data_getter import get_option_chain, get_option_exp_date, get_price, pick_vertical_put_spreads
from option_trader.utils.calc_prob import predicted_list,calc_prob_between
import numpy as np

import logging

top_pick_schema =  "symbol TEXT,strategy TEXT,exp_date TEXT,spread REAL,open_price REAL,\
                    breakeven_l REAL,breakeven_h REAL,max_profit REAL,max_loss REAL,margin REAL,\
                    pnl REAL,win_prob REAL, trade_stock_price REAL, legs_desc TEXT,\
                    target_low REAL,target_high REAL,pick_date, pick_straytegy TEXT, pick_timestamp REAL\
                    PRIMARY KEY (symbol, strategy, exp_date)"       
class top_pick_col_name():
    SYMBOL           = 'symbol'
    STRATEGY         = 'strategy' 
    EXP_DATE         = 'exp_date'    
    SPREAD           = 'spread' 
    OPEN_PRICE       = 'open_price'     

    BREAKEVEN_L      = 'breakeven_l'
    BREAKEVEN_H      = 'breakeven_h'        
    MAX_PROFIT       = 'max_profit'  
    MAX_LOSS         = 'max_loss'
    MARGIN           = 'margin'
    
    PNL              = 'pnl'         
    WIN_PROB         = 'win_prob'              
    TRADE_STOCK_PRICE= 'trade_stock_price'                 
    LEGS_DESC        = 'legs_desc'
    
    TARGET_LOW       = 'target_low'
    TARGET_HIGH      = 'target_high'
    PICK_DATE        = 'pick_date'      
    PICK_STRATEGY    = 'pick_strategy'
    PICK_TIMESTAMP   = 'pick_timestamp'

class pick_catelog():
    PREDICTED_RANGE           = 'predcicted_range' # Technical Trend Based selection
    MAX_LOSS_REALTIME         = 'max_loss_realtime'
    MAX_LOSS_PERCENT_REALTIME = 'max_loss_percent_realtime'
    MAX_LOSS_PERIOD           = 'max_loss_period'
    MAX_LOSS_PERCENT_PERIOD   = 'max_loss_percent_reriod'    

import logging
from option_trader.settings import app_settings
from option_trader.consts import asset
from option_trader.admin import site
import pandas as pd  

import os
import sqlite3


class top_pick_mgr():

    def __init__(self, this_site):
        self.this_site = this_site 
        self.logger = logging.getLogger(__name__)

        self.db_path = os.path.join(self.this_site.site_root, 'top_pick.db')
        if os.path.exists(self.db_path ) == False:
            self.db_conn = sqlite3.connect(self.db_path)        
            cursor = self.db_conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS top_pick_table ("+top_pick_schema+")")
            self.db_conn.commit()
        else:
            self.db_conn = sqlite3.connect(self.db_path)   
        
    def get_top_pick_df(self, symbol_list, pick_strategy=pick_catelog.PREDICTED_RANGE):  

        if pick_strategy == pick_catelog.PREDICTED_RANGE:
            return self.get_top_pick_df_predicted_range(symbol_list)

        elif pick_strategy == pick_catelog.MAX_LOSS_REALTIME:            
            return self.get_top_pick_df_max_loss_realtime(symbol_list)

        elif pick_strategy == pick_catelog.MAX_LOSS_PERCENT_REALTIME:            
            return self.get_top_pick_df_max_loss_percent_realtime(symbol_list)
        
        return pd.DataFrame()
        
    def get_top_pick_df_max_loss_percent_realtime(self, symbol_list):        
        df = self.this_site.get_monitor_df(filter=symbol_list)    
        df = df[df['trend'] != 'decreasing']        
        df = df[df['day change%'] < -1]
        if df.shape[0] == 0:
           self.logger.info('No symbol loss than 1%')           
           return pd.DataFrame()
        df.sort_values(by = ['day change%'], ascending=True, inplace=True)        
        symbol = df.head(1)['symbol'].values[0]    
        stock_price = get_price(symbol)
        exp_date_list = get_option_exp_date(symbol) #, min_days_to_expire=risk_mgr.open_min_days_to_expire, max_days_to_expire=runtime_config.max_days_to_expire)
        exp_date = exp_date_list[0]
        predictlist = predict_price_range(symbol, target_date_list=[exp_date])  
        predictlist[exp_date]['low'] = stock_price
        predList = predicted_list(symbol, exp_date)
        predictlist[exp_date]['win_prob'] =calc_prob_between(predList, predictlist[exp_date]['high'], predictlist[exp_date]['low'])            
        df = pick_vertical_put_spreads( symbol,                          
                                    predictlist,
                                    credit=True,
                                    max_spread = 10,
                                    max_strike_ratio=0.25,
                                    min_pnl=0.2,                                
                                    min_win_prob=np.nan,
                                    max_bid_ask_spread=np.nan,
                                    min_open_interest=0)
        df.sort_values('pnl', inplace=True)
        pick_df = df.tail(1)

        if app_settings.DATABASES == 'sqlite3':   
              
            try:
                pick_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE))                    
                pick_df[top_pick_col_name.PICK_STRATEGY] = pick_catelog.MAX_LOSS_REALTIME
                pick_df[top_pick_col_name.PICK_DATE] = pick_date.date()
                pick_df[top_pick_col_name.PICK_TIMESTAMP] = pick_date.timestamp()                
                self.write_to_db(pick_df.to_dict('records')[0])    
            except Exception as e:
                self.logger.exception(e)   
                raise e
            return pick_df             
        else:
            self.logger.error("sqlite3 only for now %s")   
            return pd.DataFrame()            

    def get_top_pick_df_max_loss_realtime(self, symbol_list):        
        df = self.this_site.get_monitor_df(filter=symbol_list)
        df = df[df['trend'] != 'decreasing']    
        df = df[df['day change%'] < -1]
        if df.shape[0] == 0:
           self.logger.info('No symbol loss than 1%')
           return pd.DataFrame()
                
        df.sort_values(by = ['day change'], ascending=True, inplace=True)   
        symbol = df.head(1)['symbol'].values[0]    
        stock_price = get_price(symbol)
        exp_date_list = get_option_exp_date(symbol) #, min_days_to_expire=risk_mgr.open_min_days_to_expire, max_days_to_expire=runtime_config.max_days_to_expire)
        exp_date = exp_date_list[0]
        predictlist = predict_price_range(symbol, target_date_list=[exp_date])  
        predictlist[exp_date]['low'] = stock_price
        predList = predicted_list(symbol, exp_date)
        predictlist[exp_date]['win_prob'] =calc_prob_between(predList, predictlist[exp_date]['high'], predictlist[exp_date]['low'])            
        df = pick_vertical_put_spreads( symbol,                          
                                    predictlist,
                                    credit=True,
                                    max_spread = 10,
                                    max_strike_ratio=0.25,
                                    min_pnl=0.2,                                
                                    min_win_prob=np.nan,
                                    max_bid_ask_spread=np.nan,
                                    min_open_interest=0)
        df.sort_values('pnl', inplace=True)
        pick_df = df.tail(1)

        if app_settings.DATABASES == 'sqlite3':   
              
            try:
                pick_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE))                    
                pick_df[top_pick_col_name.PICK_STRATEGY] = pick_catelog.MAX_LOSS_REALTIME
                pick_df[top_pick_col_name.PICK_DATE] = pick_date.date()
                pick_df[top_pick_col_name.PICK_TIMESTAMP] = pick_date.timestamp()                
                self.write_to_db(pick_df.to_dict('records')[0])    
            except Exception as e:
                self.logger.exception(e)   
                raise e
            return pick_df             
        else:
            self.logger.error("sqlite3 only for now %s")   
            return pd.DataFrame()
    
    def get_top_pick_df_predicted_range(self, symbol_list=[]):        
        pick_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE))         
        pick_strategy = pick_catelog.PREDICTED_RANGE
        if app_settings.DATABASES == 'sqlite3':   
              
            try:
                for symbol in symbol_list:
                    sql = "SELECT * FROM top_pick_table WHERE symbol='%s' AND pick_date='%s' AND pick_strategy='%s'" % (symbol, pick_date.date(), pick_strategy)
                    df = pd.read_sql_query(sql, self.db_conn)   
                    if df.shape[0] == 0:
                        self.refresh_top_picks([symbol], pick_strategy=pick_strategy)
                    else:
                        td = pick_date.timestamp() - df.head(1)[top_pick_col_name.PICK_TIMESTAMP]
                        td_mins = int(round(td / 60))
                        if td_mins > 60:
                            self.refresh_top_picks([symbol], pick_strategy=pick_strategy)                             

                df = pd.read_sql_query("SELECT * FROM top_pick_table", self.db_conn)                           
                df = df[df[asset.SYMBOL].isin(symbol_list)] if len(symbol_list)>0 else df           
                return df[(df[top_pick_col_name.PICK_STRATEGY]==pick_strategy) & (df[top_pick_col_name.PICK_DATE]==str(pick_date.date()))]
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")        

    def refresh_top_picks(self, symbol_list, pick_strategy=pick_catelog.PREDICTED_RANGE):                 
        
        if len(symbol_list) == 0:
            return
            
        pick_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())
        #remove old picks
        cursor = self.db_conn.cursor()   
        sql="DELETE FROM top_pick_table WHERE symbol in ({seq}) AND pick_date = ? AND pick_strategy = ?".format(
            seq=','.join(['?']*len(symbol_list)))
        cursor.execute(sql, symbol_list+[pick_date]+[pick_strategy])         
        self.db_conn.commit()    

        if pick_strategy==pick_catelog.PREDICTED_RANGE:    
            self.pick_by_predicted_range(symbol_list)
        
    def pick_by_predicted_range(self, symbol_list):
        pick_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE))

        picked_df = pd.DataFrame()

        for symbol in symbol_list:
            df = get_watchlist_trade_targets([symbol], st.ALL_STRATEGY)             
            if df.shape[0] == 0:
                continue
            df[top_pick_col_name.PICK_STRATEGY] = pick_catelog.PREDICTED_RANGE
            df[top_pick_col_name.PICK_DATE] = pick_date.date()
            df[top_pick_col_name.PICK_TIMESTAMP] = pick_date.timestamp()

            exp_date_list = df[pscl.EXP_DATE].unique()
            for exp_date in exp_date_list:
                de = df[df[pscl.EXP_DATE]==exp_date]            
                strategy_list = de[pscl.STRATEGY].unique()
                for strategy in strategy_list:
                    pick = de[de[pscl.STRATEGY]==strategy]            
                    if pick.shape[0] > 0:
                        pick.sort_values([pscl.WIN_PROB, pscl.PNL], ascending=False, inplace = True)
                        self.write_to_db(pick.head(1).to_dict('records')[0])                         
                        picked_df = pd.concat([picked_df, pick ])

            return picked_df
                                
    class optionLegDesc():
        def __init__(self, leg):
            self.strike             = leg[pcl.STRIKE]
            self.otype              = leg[pcl.OTYPE] 
            self.open_action        = leg[pcl.OPEN_ACTION]
            self.exp_date           = leg[pcl.EXP_DATE]
            self.scale              = leg[pcl.SCALE]
            self.price              = leg[quote.PRICE]
            self.impliedVolatility  = leg[quote.IMPLIED_VOLATILITY]
            self.delta              = leg[quote.DELTA]     
            self.gamma              = leg[quote.GAMMA]
            self.theta              = leg[quote.THETA]
            self.vega               = leg[quote.VEGA]
            self.volume             = leg[quote.VOLUME]  
            self.openInterest       = leg[quote.OPEN_INTEREST]
            
    def write_to_db(self, s):

        cl = top_pick_col_name
        import json

        legdesc = []
        exp_date =s[cl.EXP_DATE]
        legs = s[cl.LEGS_DESC]
        for leg in legs:
            legdesc.append(json.dumps(vars(self.optionLegDesc(leg))))            

        legs_dump = json.dumps(legdesc)

        #pick_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)))  

        field_names =  "'symbol', 'strategy', 'exp_date', 'spread', 'open_price',\
                        'breakeven_l','breakeven_h','max_profit','max_loss','margin',\
                        'pnl','win_prob', 'trade_stock_price','legs_desc',\
                        'target_low', 'target_high', 'pick_date', 'pick_strategy', 'pick_timestamp'"   

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' 


        fields = [s[cl.SYMBOL], s[cl.STRATEGY], s[cl.EXP_DATE], s[cl.SPREAD], s[cl.OPEN_PRICE],\
                  s[cl.BREAKEVEN_L], s[cl.BREAKEVEN_H], s[cl.MAX_PROFIT], s[cl.MAX_LOSS], s[cl.MARGIN],\
                  s[cl.PNL], s[cl.WIN_PROB], s[cl.TRADE_STOCK_PRICE], legs_dump,\
                  s[cl.TARGET_LOW], s[cl.TARGET_HIGH], s[cl.PICK_DATE], s[cl.PICK_STRATEGY], s[cl.PICK_TIMESTAMP]] 
        
        sql = "INSERT OR REPLACE INTO  top_pick_table ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()       
        cursor.execute(sql, fields)
        self.db_conn.commit()    


if __name__ == '__main__':

    import sys
    
    from option_trader.admin.site import site

    sys.path.append(r'\\Users\\jimhu\\option_trader\src')

    mysite = site('mysite')

    tp =  top_pick_mgr(mysite)

    print(tp.refresh_top_picks(['MSFT'])) #mysite.get_monitor_list()))

    print(tp.get_top_pick_df(['MSFT']))
