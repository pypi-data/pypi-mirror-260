import os
import math
import json
import sqlite3
import logging
import pandas   as pd
import numpy    as np
from   datetime import time, date, datetime, timedelta
from   pytz     import timezone
import uuid     as UUID
from   dateutil.parser import parse

from option_trader.settings import app_settings 
from option_trader.settings import ib_settings

from option_trader.settings.trade_config import entryCrit, riskManager, runtimeConfig, marketCondition
from option_trader.settings import schema as schema  
from option_trader.consts   import asset
from option_trader.consts   import strategy as st

from option_trader.utils.data_getter_ib   import place_ib_order
from option_trader.entity.position_summary import position_summary_col_name as pscl
from option_trader.entity.position         import position_col_name as pcl

from option_trader.entity import transaction
from option_trader.entity import position_summary
from option_trader.entity import position

from option_trader.entity import quote


from option_trader.utils.data_getter import pick_option_long, pick_option_short, afterHours
from option_trader.utils.data_getter import get_price, get_price_history,get_option_leg_details 
from option_trader.utils.data_getter import pick_vertical_call_spreads, pick_vertical_put_spreads
from option_trader.utils.data_getter import pick_call_butterfly, pick_put_butterfly, pick_iron_butterfly
from option_trader.utils.data_getter import pick_iron_condor, get_next_earning_date, get_option_exp_date
from option_trader.utils.predictor   import predict_price_range  
from option_trader.utils.calc_prob   import calc_win_prob

from option_trader.utils.data_getter_ib import ib_daily_account_summary_col_name, ib_daily_account_summary_schema
from option_trader.utils.data_getter_ib import ib_exceution_details_col_name, ib_execution_details_schema
from option_trader.utils.data_getter_ib import ib_completed_order_col_name, ib_completed_order_schema


account_profile_schema = "user_name TEXT, account_name TEXT NOT NULL PRIMARY KEY,initial_balance REAL,risk_mgr TEXT, entry_crit TEXT,\
        market_condition TEXT, runtime_config TEXT, default_strategy_list TEXT, default_watchlist TEXT, default_predictor TEXT,\
        open_date, FOREIGN KEY(user_name) REFERENCES user(name)"   

account_daily_summary_schema = "'Initial Balance' REAL, 'Acct Value' REAL, 'Asset Value' REAL,'Cash' REAL,\
                            'Margin' REAL,'Unrealized PL' REAL,'Realized PL' REAL, 'Risk Ratio' REAL,\
                            'Max Risk' REAL, 'Gain' REAL, 'Trx # (all)' INTEGER, 'Win Rate (all)' REAL,\
                            'Avg Loss (all)' REAL, 'Avg Win (all)' REAL,'Trx# (opened)' INEGER,\
                            'Win Rate (opened)' REAL, 'Avg Loss (opened)' REAL, 'Avg Win (opened)' REAL,\
                            'Trx# (closed)' INTEGER,'Win Rate (closed)' REAL, 'Avg Win (closed)' REAL,\
                            'Avg Loss (closed)' REAL, 'record date' TEXT NOT NULL PRIMARY KEY"

class summary_col_name():
    INIT_BALANCE            = 'Initial Balance'
    ACCT_VALUE              = 'Acct Value'
    ASSET_VALUE             = 'Asset Value'
    CASH                    = 'Cash'
    MARGIN                  = 'Margin'
    UNREALIZED_PL           = 'Unrealized PL'
    REALIZED_PL             = 'Realized PL'  
    RISK_RATIO              = 'Risk Ratio'
    MAX_RISK                = 'Max Risk'      
    GAIN                    = 'Gain'
    ALL_TRX_CNT             = 'Trx # (all)'
    ALL_WIN_RATE            = 'Win Rate (all)'    
    AVG_ALL_TRX_LOSS_PL     = 'Avg Loss (all)'
    AVG_ALL_TRX_WIN_PL      = 'Avg Win (all)'
    OPENED_TRX_CNT          = 'Trx# (opened)'
    OPENED_WIN_RATE         = 'Win Rate (opened)'       
    AVG_OPENED_TRX_LOSS_PL  = 'Avg Loss (opened)'
    AVG_OPENED_TRX_WIN_PL   = 'Avg Win (opened)'
    CLOSED_TRX_CNT          = 'Trx# (closed)'
    CLOSED_WIN_RATE         = 'Win Rate (closed)'       
    AVG_CLOSED_TRX_WIN_PL   = 'Avg Win (closed)'
    AVG_CLOSED_TRX_LOSS_PL  = 'Avg Loss (closed)'
class account():

    def __init__(self, 
                 user, 
                 account_name, 
                 initial_balance=app_settings.DEFAULT_ACCOUNT_INITIAL_BALANCE,
                 watchlist=[],
                 strategy_list=[]):        
        
        self.user = user
        self.account_name = account_name        
        self.logger = logging.getLogger(__name__) 
        
        if app_settings.DATABASES == 'sqlite3':
            try:
                self.brokerage        = self.user.get_brokerage()                
                self.db_path = os.path.join(user.user_home_dir,account_name+"_account.db")                           
                if os.path.exists(self.db_path) : 
                    self.db_conn  = sqlite3.connect(self.db_path)                     
                    self.strategy_list    = self.get_default_strategy_list()             
                    self.watchlist        = self.get_default_watchlist()                                         
                    self.entry_crit       = self.get_default_entry_crit()
                    self.risk_mgr         = self.get_default_risk_mgr()
                    self.runtime_config   = self.get_default_runtime_config()
                    self.market_condition = self.get_default_market_condition()
                    self.initial_balace   = self.get_initial_balance()
                    if self.risk_mgr.schema_updated:
                       self.update_default_risk_mgr(self.risk_mgr)            
                       self.risk_mgr.schema_updated = False
                    return
                else:
                # new account                 
                    try:
                        self.db_conn  = sqlite3.connect(self.db_path)  
                        cursor = self.db_conn.cursor()                             
                        open_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())         
                        cursor.execute("CREATE TABLE IF NOT EXISTS account_profile("+account_profile_schema+")")                        #cursor.execute("CREATE TABLE IF NOT EXISTS account_history("+account_history_schema+")")                    
                        cursor.execute("CREATE TABLE IF NOT EXISTS account_daily_summary("+account_daily_summary_schema+")")                    
                        cursor.execute("CREATE TABLE IF NOT EXISTS position_summary("+position_summary.schema+")")
                        cursor.execute("CREATE TABLE IF NOT EXISTS position("+position.schema+")")
                        cursor.execute("CREATE TABLE IF NOT EXISTS transactions("+transaction.schema+")")

                        self.strategy_list = user.default_strategy_list if len(strategy_list) == 0 else strategy_list
                        self.watchlist = user.default_watchlist if len(watchlist) == 0 else watchlist

                        self.entry_crit = entryCrit()
                        self.risk_mgr = riskManager()
                        self.runtime_config = runtimeConfig()
                        self.market_condition = marketCondition()
                        sql = "INSERT INTO account_profile (user_name, account_name, initial_balance, default_strategy_list, entry_crit, runtime_config, risk_mgr, market_condition, default_watchlist, open_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"              
                        cursor.execute(sql, [user.user_name, 
                                            account_name, 
                                            initial_balance,
                                            json.dumps(self.strategy_list),
                                            json.dumps(vars(entryCrit())),
                                            json.dumps(vars(runtimeConfig())),
                                            json.dumps(vars(riskManager())),
                                            json.dumps(vars(marketCondition())),
                                            json.dumps(self.watchlist),
                                            open_date                                     
                                        ])               
                        sql = 'INSERT INTO position (symbol, current_value) VALUES(?,?)' 
                        cursor.execute(sql, [asset.CASH, initial_balance])
                        cursor.execute(sql, [asset.MARGIN, 0])                
                        self.cash_position = initial_balance
                        self.margin_position = 0
                        self.db_conn.commit()       
                    except Exception as e:
                        self.logger.exception(e)
                        import shutil
                        if os.path.exists(self.db_path):
                            shutil.rmtree(self.db_path)                      
                        raise e                        
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('unsupported database engine %s' % app_settings.DATABASES)

    def __enter__(self):
        return self
  
    def __exit__(self, *args):
        try:
            self.db_conn.close()
        except Exception as ex:
            self.logger.exception(ex)
            raise ex

    def update_ib_position(self):

        return self.update_ib_position_summary()
 
    def update_ib_position_summary(self):
          
        today = datetime.now(timezone(app_settings.TIMEZONE))
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")   
        sdf = pd.read_sql_query("SELECT * FROM position_summary WHERE status = '"+asset.OPENED+"'", self.db_conn)

        uuid_list = sdf[pscl.UUID].unique()      

        trade_rec_list = []

        for uuid in uuid_list:       
            if uuid == None:
                continue

            srow        = sdf[sdf[pscl.UUID]==uuid].iloc[0]
            symbol      = srow[pscl.SYMBOL]
            strategy    = srow[pscl.STRATEGY]             
            quantity    = srow[pscl.QUANTITY]
            if quantity  == 0:
                continue

            ppdf = pd.read_sql_query("SELECT * FROM ib_account_portfolio WHERE uuid = '"+uuid+"'", self.db_conn)
            if ppdf.shape[0] == 0:
                self.logger.error("No position found for UUID=%s" % uuid)
                continue
            
            stock_price     = get_price(symbol)        
            gain            = srow[pscl.GAIN] #open_price - last_price if credit else last_price - open_price            
            pl              = srow[pscl.PL] #gain * quantity
            exp_date        = srow[pscl.EXP_DATE]
            last_win_prob   = srow[pscl.LAST_WIN_PROB]
            open_price      = srow[pscl.OPEN_PRICE]
            last_price      = srow[pscl.LAST_PRICE]

            days_to_expire  = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days+1                                  
            stopped = False
            roll = False
            if gain >= self.risk_mgr.stop_gain_percent:
                stopped = True
                stop_reason = 'Stop Gain %.2f >= %.2f'% (gain, self.risk_mgr.stop_gain_percent)            
                if days_to_expire > 5:
                    roll = True
            elif gain < 0 and abs(gain) >= self.risk_mgr.stop_loss_percent:
                stopped = True            
                stop_reason =  'Stop Loss %.2f >= %.2f'  % (gain, self.risk_mgr.stop_loss_percent)    
                if days_to_expire > 5:
                    roll = True
            elif days_to_expire <= self.risk_mgr.close_days_before_expire:
                stopped = True   
                stop_reason = 'Days to expire %d <= %d' % (days_to_expire, self.risk_mgr.close_days_before_expire)            
            elif last_win_prob < 10:
                stopped = True   
                stop_reason = 'Last Win Prob %.2f <= 10' % (last_win_prob)                          
            else:
                try:
                    datetime.fromisoformat(srow[pscl.EARNING_DATE])
                    earning_date = pd.Timestamp(srow[pscl.EARNING_DATE]).tz_convert(timezone(app_settings.TIMEZONE))                 
                    days_to_earning = (earning_date - today).days+1               
                    if days_to_earning <= self.risk_mgr.close_days_before_expire:
                        stopped = True                           
                        stop_reason = 'Days to earning %d <= %d'  % (days_to_earning, self.risk_mgr.close_days_before_expire)    
                except ValueError:
                     pass                   

            if stopped:           

                self.close_ib_position(srow, ppdf)
                if len(srow.ib_errorString) > 0:
                    msg = "STOP FAILED  %s errorCode %s [%s|%s|%s|%d] [reason:%s|gain:%.2f|op:%.2f|lp:%.2f|pl:%.2f|wp:%.2f][%s]" %\
                                (srow.ib_errorString, str(srow.ib_errorCode), strategy, symbol, exp_date, quantity, stop_reason, gain, open_price, last_price, pl, last_win_prob, self.account_name)                                           
                    self.logger.error(msg)    
                    sql = """update position_summary set ib_errorString=?, ib_errorCode=?, ib_status=? where uuid==?"""        
                    data = (srow.ib_errorString, srow.ib_errorCode, srow.ib_status, uuid)                     
                else:
                    status = asset.CLOSE_PENDING                    
                    msg = "STOP  [%s|%s|%s|%d] [reason:%s|gain:%.2f|op:%.2f|lp:%.2f|pl:%.2f|wp:%.2f][%s]" %\
                                (strategy, symbol, exp_date, quantity, stop_reason, gain, open_price, last_price, pl, last_win_prob, self.account_name)                       
                    self.logger.info(msg)       
                    sql = """update position_summary set status=?, ib_status=? where uuid==?"""        
                    data = (status, srow.ib_status, uuid)       

                cursor = self.db_conn.cursor()    
                cursor.execute(sql, data)     
                self.db_conn.commit()  
              
                trade_rec_list.append(msg)

        return trade_rec_list

    def close_ib_position(self, srow, ppdf):     
        symbol      = srow[pscl.SYMBOL]
        quantity    = srow[pscl.QUANTITY]       
        strategy    = srow[pscl.STRATEGY]
        exp_date    = srow[pscl.EXP_DATE]

        legs = []
        for i, l in ppdf.iterrows():
            leg = {}
            leg[pcl.OTYPE] = asset.CALL if l['right'] == 'C' else asset.PUT
            leg[pcl.EXP_DATE] = exp_date
            leg[pcl.STRIKE] = l.strike
            leg[pcl.SCALE] = 1           
            leg[pcl.OPEN_ACTION] = asset.BUY_TO_CLOSE if l['position'] < 0 else asset.SELL_TO_CLOSE
            legs.append(leg)

        srow[pscl.LEGS] = legs

        live = False if 'PAPER' in self.brokerage else True
        place_ib_order(srow, TWS=ib_settings.TWS, live=live, bracket=False, orderType='MKT', orderAction='Close')
        if len(srow.ib_errorString) > 0:
            msg = "CLOSE IB_ORDER FAILED %s errorCode %s [%s|%s|%s] [q:%d] [legs:%s] [accnt:%s]" %\
                (srow.ib_errorString, str(srow.ib_errorCode), strategy, symbol, exp_date, quantity, str(legs), self.account_name)
            self.logger.error(msg)
        
        return
    
    def get_ib_unpaired(self, stock_df, ib_portfolio_df):

        unpaired_df = pd.DataFrame()

        for i, p in stock_df.iterrows():
            if p.position == 0:
                continue
            uuid  = UUID.uuid4().hex        
            index = unpaired_df.shape[0]               
            unpaired_df.at[index, pscl.UUID] = uuid                  
            ib_portfolio_df.at[i, pscl.UUID] = uuid            
            stock_price = get_price(p.symbol)        
            unpaired_df.at[index, pscl.SYMBOL] = p.symbol  
            unpaired_df.at[index, pscl.QUANTITY] = quantity = abs(p.position)   
            unpaired_df.at[index, pscl.STRATEGY] = st.UNPAIRED
            unpaired_df.at[index, pscl.EXP_DATE] = ""            
            unpaired_df.at[index, pscl.SPREAD] = np.nan   
            credit = True if p.position < 0 else False  
            unpaired_df.at[index, pscl.CREDIT] = str(credit)
            unpaired_df.at[index, pscl.MAX_PROFIT] = p.averageCost if credit else (stock_price*1.5) - p.averageCost              
            unpaired_df.at[index, pscl.MAX_LOSS] = ((stock_price*1.5)) - p.averageCost if credit else p.averageCost            
            unpaired_df.at[index, pscl.OPEN_PRICE] =  p.averageCost  if p.position > 0 else -1 * p.averageCost          
            unpaired_df.at[index, pscl.LAST_PRICE] =  p.marketValue/quantity  
            unpaired_df.at[index, pscl.PL] = p.unrealizedPNL     
            unpaired_df.at[index, pscl.PNL] = unpaired_df.at[index, pscl.MAX_PROFIT] / unpaired_df.at[index, pscl.MAX_LOSS]
            unpaired_df.at[index, pscl.GAIN] = 100 *(p.unrealizedPNL/p.totalCost)   
            
            breakeven_l = np.nan if credit else round(p.averageCost,2) 
            breakeven_h =  round(p.averageCost,2) if credit else np.nan

            today = datetime.now(timezone(app_settings.TIMEZONE))        
            from dateutil.relativedelta import relativedelta        
            three_mon_rel = relativedelta(months=12)
            target_date = str((today + three_mon_rel).date()) 
            last_win_prob = calc_win_prob(p.symbol, target_date, st.UNPAIRED, breakeven_l, breakeven_h)    
            unpaired_df.at[index, pscl.LAST_WIN_PROB] = last_win_prob  
            unpaired_df.at[index, pscl.BREAKEVEN_H] = breakeven_h  
            unpaired_df.at[index, pscl.BREAKEVEN_L] = breakeven_l  

        return unpaired_df
    
    def get_ib_single_leg(self, o, ib_portfolio_df):        
        single_df = pd.DataFrame()
        for i, p in o.iterrows():
            if p.position == 0:
                continue
            index = single_df.shape[0]

            uuid  = UUID.uuid4().hex        
            single_df.at[index, pscl.UUID] = uuid                  
            ib_portfolio_df.at[i, pscl.UUID] = uuid              

            stock_price = get_price(p.symbol)        
            single_df.at[index, pscl.SYMBOL] = p.symbol
            single_df.at[index, pscl.EXP_DATE] = parse(p.exp_date).strftime('%Y-%m-%d')    
            single_df.at[index, pscl.SPREAD] = np.nan            
            single_df.at[index, pscl.QUANTITY] = quantity = abs(p.position)          
            credit = True if p.position < 0 else False    
            single_df.at[index, pscl.CREDIT] = str(credit)
            if p.right == 'C':
                single_df.at[index, pscl.STRATEGY] = st.COVERED_CALL if credit else st.LONG_CALL
                single_df.at[index, pscl.MAX_PROFIT] = p.averageCost / 100 if credit else (((stock_price*1.5)-p.strike)) - (p.averageCost/100)  
                single_df.at[index, pscl.MAX_LOSS] = ((p.strike-(stock_price*0.5))) - (p.averageCost/100) if credit else p.averageCost / 100           
            else:
                single_df.at[index, pscl.STRATEGY] = st.SHORT_PUT if credit else st.LONG_PUT
                single_df.at[index, pscl.MAX_PROFIT] = p.averageCost / 100 if credit else ((p.strike-(stock_price*0.5))) - (p.averageCost/100)              
                single_df.at[index, pscl.MAX_LOSS] = (((stock_price*1.5)-p.strike)) - (p.averageCost/100) if credit else p.averageCost /100            
                
            single_df.at[index, pscl.OPEN_PRICE] =  p.averageCost / 100 if p.position > 0 else -1 * (p.averageCost / 100)          
            single_df.at[index, pscl.LAST_PRICE] =  p.marketValue/(quantity*100)  
            single_df.at[index, pscl.PL] = p.unrealizedPNL     
            single_df.at[index, pscl.PNL] = single_df.at[index, pscl.MAX_PROFIT] / single_df.at[index, pscl.MAX_LOSS]
            single_df.at[index, pscl.GAIN] = 100 *(p.unrealizedPNL/p.totalCost)   

            if p.right == 'C':
                breakeven_h =  round(p.strike-single_df.at[index, pscl.OPEN_PRICE],2) if credit else np.nan     
                breakeven_l =  np.nan if credit else round(p.strike-single_df.at[index, pscl.OPEN_PRICE],2)
            else:      
                breakeven_l =  round(p.strike-single_df.at[index, pscl.OPEN_PRICE],2) if credit else np.nan
                breakeven_h =  np.nan if credit else round(p.strike-single_df.at[index, pscl.OPEN_PRICE],2) 

            last_win_prob = calc_win_prob( p.symbol, single_df.at[index, pscl.EXP_DATE], single_df.at[index, pscl.STRATEGY], breakeven_l, breakeven_h)  
            single_df.at[index, pscl.LAST_WIN_PROB] = last_win_prob  
            single_df.at[index, pscl.BREAKEVEN_H] = breakeven_h  
            single_df.at[index, pscl.BREAKEVEN_L] = breakeven_l  

        return single_df  

    def get_ib_spread(self, n, q, ni, qi,ib_portfolio_df):

        spread_df = pd.DataFrame()

        uuid  = UUID.uuid4().hex        
        spread_df.at[0, pscl.UUID] = uuid                  
        ib_portfolio_df.at[ni, pscl.UUID] = uuid   
        ib_portfolio_df.at[qi, pscl.UUID] = uuid           
        spread_df.at[0, pscl.SYMBOL] = n.symbol
        spread_df.at[0, pscl.EXP_DATE] = parse(n.exp_date).strftime('%Y-%m-%d')    
        spread_df.at[0, pscl.QUANTITY] = quantitiy = abs(min(n.position, q.position))       
        spread_df.at[0, pscl.SPREAD] = spread = abs(n.strike-q.strike)    
        credit = True if n.totalCost + q.totalCost < 0 else False    
        spread_df.at[0, pscl.CREDIT] = str(credit)
        if n.right == 'C':
            spread_df.at[0, pscl.STRATEGY] = st.CREDIT_CALL_SPREAD if credit else st.DEBIT_CALL_SPREAD
        else:
            spread_df.at[0, pscl.STRATEGY] = st.CREDIT_PUT_SPREAD if credit else st.DEBIT_PUT_SPREAD
            
        spread_df.at[0, pscl.OPEN_PRICE] =  (n.totalCost + q.totalCost)/(quantitiy*100)           
        spread_df.at[0, pscl.LAST_PRICE] =  (n.marketValue + q.marketValue)/(quantitiy*100)  
        spread_df.at[0, pscl.PL] = (n.unrealizedPNL + q.unrealizedPNL)      
        spread_df.at[0, pscl.MAX_PROFIT] = -1 * (n.totalCost + q.totalCost) / quantitiy / 100 if credit else (spread - spread_df.at[0, pscl.OPEN_PRICE])  
        spread_df.at[0, pscl.MAX_LOSS] = spread - spread_df.at[0, pscl.MAX_PROFIT] if credit else spread_df.at[0, pscl.OPEN_PRICE]
        spread_df.at[0, pscl.PNL] =  spread_df.at[0, pscl.MAX_PROFIT] / spread_df.at[0, pscl.MAX_LOSS]  
        spread_df.at[0, pscl.GAIN] = 100 * spread_df.at[0, pscl.PL] /  abs(n.totalCost + q.totalCost) 
        short_strike = n.strike if n.position < 0 else q.strike
        long_strike = n.strike if n.position > 0 else q.strike

        if n.right == 'C':
            breakeven_h = short_strike + spread_df.at[0, pscl.OPEN_PRICE] if credit else np.nan
            breakeven_l = np.nan if credit else long_strike + spread_df.at[0, pscl.OPEN_PRICE]                     
        else:    
            breakeven_l = short_strike - spread_df.at[0, pscl.OPEN_PRICE] if credit else np.nan
            breakeven_h = np.nan  if credit else  long_strike - spread_df.at[0, pscl.OPEN_PRICE]      

        last_win_prob = calc_win_prob( n.symbol, spread_df.at[0, pscl.EXP_DATE], spread_df.at[0, pscl.STRATEGY], breakeven_l, breakeven_h)  
        spread_df.at[0, pscl.LAST_WIN_PROB] = last_win_prob  
        spread_df.at[0, pscl.BREAKEVEN_H] = breakeven_h  
        spread_df.at[0, pscl.BREAKEVEN_L] = breakeven_l  
        
        return spread_df

    def load_ib_porforlio(self, ib_portfolio_df):

        ib_portfolio_df['totalCost'] = ib_portfolio_df.apply(lambda x: x['position'] * x['averageCost'],axis=1)
        stock_df  = ib_portfolio_df[(ib_portfolio_df['secType'] == 'STK') & (ib_portfolio_df['position'] != 0)]
        option_df = ib_portfolio_df[(ib_portfolio_df['secType'] == 'OPT') & (ib_portfolio_df['position'] != 0)]

        pos_summary_df = pd.DataFrame()
        if stock_df.shape[0] > 0:
            pos_summary_df = pd.concat([pos_summary_df, self.get_ib_unpaired(stock_df, ib_portfolio_df)])

        if option_df.shape[0] == 0:
            return pos_summary_df            
        
        x = option_df.groupby(by=['symbol', 'exp_date', 'right'])

        for name, group in x:
            symbol, exp_date, right = name
            ng = group[group['position'] < 0]
            pg = group[group['position'] > 0]
            for i, n in ng.iterrows(): 
                if n.position == 0:
                    continue

                for j, p in pg.iterrows():
                    if p.position == 0:
                        continue

                    if p.position == -1 * n.position:                            
                        pos_summary_df = pd.concat([pos_summary_df, self.get_ib_spread(n, p, i, j, ib_portfolio_df)])                
                        pg = pg.drop([j], axis='index')
                        ng.at[i, 'position'] = 0     
                        pg.at[j, 'position'] = 0                               
                        break                    
                    elif p.position > -1 * n.position:                      
                        opos = pg.at[j, 'position']
                        p.position += n.position
                        ratio = p.position / opos                
                        p.totalCost = p.totalCost * ratio 
                        p.marketValue = p.marketValue * ratio 
                        p.unrealizedPNL = p.unrealizedPNL * ratio                   
                        pos_summary_df = pd.concat([pos_summary_df, self.get_ib_spread(n, p, i, j, ib_portfolio_df)])  
                        ng.at[i, 'position'] = 0     
                        opos = pg.at[j, 'position']
                        ratio = (opos + n.position) / opos                   
                        pg.at[j, 'position'] = (opos + n.position)        
                        pg.at[j, 'totalCost'] = pg.at[j, 'totalCost'] * ratio 
                        pg.at[j, 'marketValue'] = pg.at[j, 'marketValue'] * ratio 
                        pg.at[j, 'unrealizedPNL'] = pg.at[j, 'unrealizedPNL'] * ratio                                   
                        break
                    else:              
                        opos = n.position
                        n.position = -1 * p.position                 
                        ratio = n.position / opos
                        n.totalCost = n.totalCost * ratio 
                        n.marketValue = n.marketValue * ratio 
                        n.unrealizedPNL = n.unrealizedPNL * ratio                        
                        pos_summary_df = pd.concat([pos_summary_df, self.get_ib_spread(n, p, i, j, ib_portfolio_df)])        
                        n.position = opos + p.position                 
                        #ng.at[i, 'position'] = n.position               
                        ratio = n.position / opos
                        ng.at[i, 'position']  = n.totalCost * ratio 
                        ng.at[i, 'totalCost'] = n.marketValue * ratio 
                        ng.at[i, 'unrealizedPNL'] = n.unrealizedPNL * ratio
                        n.totalCost = n.totalCost * ratio 
                        n.marketValue = n.marketValue * ratio 
                        n.unrealizedPNL = n.unrealizedPNL * ratio      
                        ng.at[i, 'position'] = n.position               
                        pg.at[j, 'position'] = 0       

            pos_summary_df = pd.concat([pos_summary_df, self.get_ib_single_leg(pd.concat([ng, pg]), ib_portfolio_df)])
                
        self.create_ib_position_summary(pos_summary_df)
        
        return ib_portfolio_df
    
    def create_ib_position_summary(self, summary_df):

        sql = "DELETE FROM position_summary WHERE status = 'opened'" 
        self.db_conn.execute(sql)         

        for i, row in summary_df.iterrows():
            #uuid        = UUID.uuid4().hex
            uuid        = row[pscl.UUID]            
            symbol      = row[pscl.SYMBOL]
            exp_date    = row[pscl.EXP_DATE]
            strategy    = row[pscl.STRATEGY]
            quantity    = row[pscl.QUANTITY]
            open_price  = round(abs(row[pscl.OPEN_PRICE]),2) 
            max_profit  = round(row[pscl.MAX_PROFIT],2)
            max_loss    = round(row[pscl.MAX_LOSS],2)
            pnl         = round(row[pscl.PNL],2) 
            pl          = round(row[pscl.PL],2)             
            spread      = row[pscl.SPREAD]        
            credit      = row[pscl.CREDIT] 
            status      = asset.OPENED        
            gain        = round(row[pscl.GAIN],2) 
            last_price  = round(row[pscl.LAST_PRICE],2) 

            today = datetime.now(timezone(app_settings.TIMEZONE))

            last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z") 
            last_stock_price = round(get_price(symbol),2)
            breakeven_l      = row[pscl.BREAKEVEN_L]
            breakeven_h      = row[pscl.BREAKEVEN_H] 
            last_win_prob    = row[pscl.LAST_WIN_PROB]       
            credit           = row[pscl.CREDIT] 

            r = self.user.site.get_monitor_rec(symbol)
            if len(r) > 0:
                target_low   = r['target_low']
                target_high  = r['target_high']
                earning_date = r['earning']                 
            else:
                target_low = target_high = np.nan
                try:
                    earning_date = get_next_earning_date(symbol)
                    earning_date = "" if earning_date == None else str(earning_date)
                except Exception as ex:
                    self.logger.exception

            fields = [uuid, symbol, strategy, credit, spread,\
                      open_price, exp_date,max_profit, max_loss, pnl,\
                      earning_date,quantity,status, last_price, pl,\
                      gain, last_quote_date, last_stock_price, target_high, target_low,\
                      breakeven_h, breakeven_l, last_win_prob]

            field_names =  "uuid,symbol,strategy,credit,spread,\
                            open_price,exp_date,max_profit,max_loss,pnl,\
                            earning_date,quantity,status,last_price, pl,\
                            gain, last_quote_date, last_stock_price, target_high, target_low,\
                            breakeven_h, breakeven_l, last_win_prob "        
            
            values =  '?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?'                     
            sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)

        self.db_conn.commit()    

    def get_ib_account_values(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:          
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_account_values' not in table_names:
                    return pd.DataFrame()                       
                return pd.read_sql_query("SELECT * FROM ib_account_values", self.db_conn)              
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_account_values(self, accountValues_dict):  
        if app_settings.DATABASES == 'sqlite3':                 
            try:                  
                df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in accountValues_dict.items()]))                                              
                df.to_sql('ib_account_values', self.db_conn, if_exists='replace', index=False)
                return df            
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_ib_daily_account_summary(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:              
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_daily_account_summary' not in table_names:
                    return pd.DataFrame()                  
                return pd.read_sql_query("SELECT * FROM ib_daily_account_summary", self.db_conn)                                                
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_daily_account_summary(self, ib_account_summary):    
 
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                cursor = self.db_conn.cursor()  
                result = cursor .execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_daily_account_summary' not in table_names:
                        cursor = self.db_conn.cursor()                                  
                        cursor.execute("CREATE TABLE IF NOT EXISTS ib_daily_account_summary("+ib_daily_account_summary_schema+")") 
                ib_account_summary[ib_daily_account_summary_col_name.RecordDate] = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())         
                members = [attr for attr in dir(ib_daily_account_summary_col_name) if not \
                            callable(getattr(ib_daily_account_summary_col_name, attr)) and not attr.startswith("__")]                                
                members.sort()
                field_names = str(members).strip("[]")           
                values = '?' + ",?" * (len(members)-1)
                fields = []
                for fld in members:
                    fields.append(ib_account_summary[fld])
                sql = "INSERT OR REPLACE INTO  ib_daily_account_summary ("+field_names+") VALUES("+values+")" 
                cursor = self.db_conn.cursor()          
                cursor.execute(sql, fields)
                self.db_conn.commit()    
            
            except Exception as e:
                self.logger.exception(e)   
                raise e
                #return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_ib_account_positions(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:            
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_positions' not in table_names:
                    return pd.DataFrame()                  
                return pd.read_sql_query("SELECT * FROM ib_positions", self.db_conn)                                               
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def drop_ib_account_positions(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                cursor = self.db_conn.cursor()                                         
                cursor.execute("DROP TABLE IF EXISTS ib_positions")
                self.db_conn.commit()
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_account_positions(self, pos_df):
        if app_settings.DATABASES == 'sqlite3':                 
            try:                                                                        
                pos_df.to_sql('ib_positions', self.db_conn, if_exists='replace', index=False)             
                return pos_df            
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")        

    def drop_ib_account_openOrders(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                cursor = self.db_conn.cursor()                                         
                cursor.execute("DROP TABLE IF EXISTS ib_open_orders")
                self.db_conn.commit()
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_ib_account_openOrders(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:              
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_open_orders' not in table_names:
                    return pd.DataFrame()                    
                return pd.read_sql_query("SELECT * FROM ib_open_order", self.db_conn)                                               
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_account_openOrders(self, orders_df):
        if app_settings.DATABASES == 'sqlite3':                 
            try:                                                                             
                orders_df.to_sql('ib_open_orders', self.db_conn, if_exists='replace', index=False)                                
                return orders_df            
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")    

    def get_ib_account_portfolio(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:                         
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_account_portfolio' not in table_names:
                    return pd.DataFrame()       
                return pd.read_sql_query("SELECT * FROM ib_account_portfolio", self.db_conn)                                               
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def drop_ib_account_portfolio(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                cursor = self.db_conn.cursor()                                         
                cursor.execute("DROP TABLE IF EXISTS ib_account_portfolio")
                self.db_conn.commit()
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_account_portfolio(self, portfolio_df):  
        if app_settings.DATABASES == 'sqlite3':                 
            try:                                                                         
                portfolio_df = self.load_ib_porforlio(portfolio_df)                 
                portfolio_df.to_sql('ib_account_portfolio', self.db_conn, if_exists='replace', index=False)              
                return portfolio_df          
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_ib_execution_details(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:  
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_execution_details' not in table_names:
                    return pd.DataFrame()
                                
                return pd.read_sql_query("SELECT * FROM ib_execution_details", self.db_conn)                                               
            
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_execution_details(self, exec_df):    

        if exec_df.shape[0] == 0:
            return
        
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_executions_details' not in table_names:
                        cursor = self.db_conn.cursor()                                  
                        cursor.execute("CREATE TABLE IF NOT EXISTS ib_execution_details("+ib_execution_details_schema+")")                                  

                members = [attr for attr in dir(ib_exceution_details_col_name) if not \
                            callable(getattr(ib_exceution_details_col_name, attr)) and not attr.startswith("__")]                                
                #members.sort()
                field_names = str(members).strip("[]")           
                values = '?' + ",?" * (len(members)-1)

                for i, row in exec_df.iterrows():
                    fields = []
                    for fld in members:
                        fields.append(row[fld])                             
                    sql = "INSERT OR REPLACE INTO  ib_execution_details ("+field_names+") VALUES("+values+")" 
                    cursor = self.db_conn.cursor()          
                    cursor.execute(sql, fields)
                    self.db_conn.commit()    
            
            except Exception as e:
                self.logger.exception(e)   
                raise e
                #return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_ib_completed_orders(self):    
        if app_settings.DATABASES == 'sqlite3':                 
            try:  
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_completed_order' not in table_names:
                    return pd.DataFrame()                                
                return pd.read_sql_query("SELECT * FROM ib_completed_order", self.db_conn)                                               
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def save_ib_completed_orders(self, completed_order_df):    

        if completed_order_df.shape[0] == 0:
            return
        
        if app_settings.DATABASES == 'sqlite3':                 
            try:
                cursor = self.db_conn.cursor()  
                result = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
                table_names = sorted(list(zip(*result))[0])
                if 'ib_completed_order' not in table_names:
                        cursor = self.db_conn.cursor()                                  
                        cursor.execute("CREATE TABLE IF NOT EXISTS ib_completed_order("+ib_completed_order_schema+")")                                  
                        self.db_conn.commit()    
                members = [attr for attr in dir(ib_completed_order_col_name) if not \
                            callable(getattr(ib_completed_order_col_name, attr)) and not attr.startswith("__")]                                

                members.sort()
                field_names = str(members).strip("[]")           
                values = '?' + ",?" * (len(members)-1)

                for i, row in completed_order_df.iterrows():
                    fields = []
                    for fld in members:
                        fields.append(row[fld])                             
                    sql = "INSERT OR REPLACE INTO  ib_completed_order ("+field_names+") VALUES("+values+")" 
                    cursor = self.db_conn.cursor()          
                    cursor.execute(sql, fields)
                    self.db_conn.commit()    
            
            except Exception as e:
                self.logger.exception(e)   
                raise e
                #return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def __update_cash_position(self, cash_position, commit=True):
        
        if app_settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "UPDATE position SET current_value = '"+str(cash_position) + "' WHERE symbol = '"+asset.CASH + "'"                              
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                if commit:
                    self.db_conn.commit()
                return cash_position                
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % app_settings.DATABASES)
            return np.nan
        
    def __update_margin_position(self, margin_position, commit=True):

        if math.isnan(margin_position):
            self.logger.error('Nan margin_position appears!!')
            return np.nan            

        if app_settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "UPDATE position SET current_value = '"+str(margin_position) + "' WHERE symbol = '"+asset.MARGIN + "'"                              
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                if commit:
                    self.db_conn.commit()      
                return margin_position    
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % app_settings.DATABASES)
            return np.nan
                    
    def get_initial_balance(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT initial_balance FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_open_date(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT open_date FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]                  
            except Exception as e:
                #self.logger.exception(e)   
                return None
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_default_strategy_list(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_strategy_list FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_default_watchlist(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_watchlist FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_default_strategy_list(self, strategy_list):
        if app_settings.DATABASES == 'sqlite3':
            try:
                sql = "UPDATE account_profile SET default_strategy_list='"+json.dumps(strategy_list)+"' WHERE account_name='"+self.account_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()      
                self.strategy_list = strategy_list                    
            except Exception as e:
                self.logger.exception(e)       
                raise e
        else:
            self.logger.error('unsupported database engine %s' % app_settings.DATABASES)

    def update_default_watchlist(self, watchlist):
        if app_settings.DATABASES == 'sqlite3':
            try:
                sql = "UPDATE account_profile SET default_watchlist='"+json.dumps(watchlist)+"' WHERE account_name='"+self.account_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()      
                self.watchlist = watchlist                    
                self.user.site.expand_monitor_list(watchlist)                
            except Exception as e:
                self.logger.exception(e)       
                raise e
        else:
            self.logger.error('unsupported database engine %s' % app_settings.DATABASES)

    def get_default_entry_crit(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT entry_crit FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return entryCrit(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def get_default_entry_crit(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT entry_crit FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return entryCrit(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
    
    def update_default_entry_crit(self, entry_crit):

        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET entry_crit='"+json.dumps(vars(entry_crit))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)          
                self.db_conn.commit()                     
                self.entry_crit = entry_crit 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
    
    def get_default_runtime_config(self):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT runtime_config FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return runtimeConfig(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def update_default_runtime_config(self, runtime_config):

        self.runtime_config = runtime_config
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET runtime_config='"+json.dumps(vars(runtime_config))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)                
                self.db_conn.commit()
                self.runtime_config = runtime_config
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def get_default_risk_mgr(self):

        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT risk_mgr FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return riskManager(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def update_default_risk_mgr(self, risk_mgr):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET risk_mgr='"+json.dumps(vars(risk_mgr))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)          
                self.db_conn.commit()
                self.risk_mgr = risk_mgr      
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
    
    def get_default_market_condition(self):

        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT market_condition FROM account_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return marketCondition(json.loads(cursor.fetchone()[0]))                 
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None

    def update_default_market_condition(self, market_condition):
        if app_settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "UPDATE account_profile SET market_condition='"+json.dumps(vars(market_condition))+"' WHERE account_name='"+self.account_name+"'"                                 
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)       
                self.db_conn.commit()
                self.market_condition = market_condition         
            except Exception as e:
                self.logger.exception(e)   
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

        return None
            
    #def get_BuyingPower(self):
        
    def get_BuyingPower(self):

        if 'IB' in self.brokerage:
            return self.get_cash_position() - self.get_margin_position()      
            
        if app_settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "SELECT current_value FROM position WHERE symbol = '"+asset.CASH+"'"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return float(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % app_settings.DATABASES)
            return np.nan

    def get_cash_position(self):

        if 'IB' in self.brokerage:
            try:
                df = self.get_ib_daily_account_summary()
                if df.shape[0] == 0:
                    self.logger.warning("%s No daily assount summary found" % self.account_name)
                    return np.nan
                return df.tail(1)['TotalCashValue'].values[0]
            except Exception as e:
                self.logger.exception(e)
                return np.nan     
            
        if app_settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "SELECT current_value FROM position WHERE symbol = '"+asset.CASH + "'"
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return float(cursor.fetchone()[0])+self.get_margin_position()                          
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % app_settings.DATABASES)
            return np.nan
                                                    
    def get_margin_position(self):

        if 'IB' in self.brokerage:
            try:
                df = self.get_ib_daily_account_summary()
                if df.shape[0] == 0:
                    self.logger.warning("%s No daily assount summary found" % self.account_name)
                    return np.nan
                return df.tail(1)['InitMarginReq'].values[0]
            except Exception as e:
                self.logger.exception(e)
                return np.nan     
            
        if app_settings.DATABASES == 'sqlite3':                    
            try:    
                sql = "SELECT current_value FROM position WHERE symbol = '"+asset.MARGIN + "'"
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return float(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported DB engine %s' % app_settings.DATABASES)
            return np.nan
    
    def get_asset_value(self):
        #brokerage = self.user.get_brokerage()
        if 'IB' in self.brokerage:
            try:
                df = self.get_ib_account_portfolio()
                if df.shape[0] == 0:
                    self.logger.warning("No portfolio found")
                    return 0

                asset_value = round(df['marketValue'].sum(),2)                
                return asset_value
            except Exception as e:
                self.logger.exception(e)
                return np.nan 
                    
        pos = self.get_positions()
        open_pos = pos[pos[pcl.STATUS]==asset.OPENED]      
        bto_df = open_pos[open_pos[pcl.OPEN_ACTION] == asset.BUY_TO_OPEN]
        sto_df = open_pos[open_pos[pcl.OPEN_ACTION] == asset.SELL_TO_OPEN]
        asset_value = bto_df[pcl.CURRENT_VALUE].sum() - sto_df[pcl.CURRENT_VALUE].sum()
        return asset_value
        
    def get_pl(self):
        if 'IB' in self.brokerage:
            try:
                df = self.get_ib_account_portfolio()
                if df.shape[0] == 0:
                    self.logger.warning("No portfolio found")
                    unreliazed_pl = 0
                else:
                    unreliazed_pl = round(df['unrealizedPNL'].sum(),2)      

                df = self.get_ib_account_values()
                if df.shape[0] == 0:
                    self.logger.warning("%s No daily assount summary found" % self.account_name)
                    realized_pl  = 0
                else:
                    realized_pl = round(float(df.tail(1)['RealizedPnL'].values[0]),2)
            
                return unreliazed_pl , realized_pl            
            except Exception as e:
                self.logger.exception(e)
                return np.nan, np.nan  
                                      
                return asset_value
            except Exception as e:
                self.logger.exception(e)
                return np.nan 
                    
        ps = self.get_position_summary(get_leg_dedail=False)
        unreliazed_pl = ps[ps[pscl.STATUS]== asset.OPENED][pscl.PL].sum()
        realized_pl = ps[ps[pscl.STATUS] != asset.OPENED][pscl.PL].sum()
        return round(unreliazed_pl,2) , round(realized_pl,2)
    
    def get_account_value(self):
        #brokerage = self.user.get_brokerage()
        if 'IB' in self.brokerage:
            try:
                df = self.get_ib_daily_account_summary()
                if df.shape[0] == 0:
                    self.logger.warning("%s No daily assount summary found" % self.account_name)
                    return np.nan
                return round(df.tail(1)['NetLiquidation'].values[0],2)
            except Exception as e:
                self.logger.exception(e)
                return np.nan     
                    
        return self.get_BuyingPower()+self.get_margin_position()+self.get_asset_value()
        
    def create_position(self, symbol, legs, q, uuid_value, trade_date):

        field_names =  "uuid,leg_id,symbol,otype,strike,exp_date,open_action,quantity,open_price,current_value,average_cost_basis,init_delta,init_IV,init_volume,init_open_interest,status,trade_date, last_price, total_gain_loss, last_quote_date, total_gain_loss_percent"

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' 

        legdesc = []
        leg_id = -1
        pos = {}
        for leg in legs:
            otype       =leg[quote.OTYPE]
            if otype == asset.STOCK: # buy write or buy with protected put
                # TO BE FIXED
                open_action =leg[quote.OPEN_ACTION]
                status = asset.OPENED
                quantity = q * 100              
                average_cost_basis = quantity * leg[quote.LAST_PRICE]                  
                current_value = average_cost_basis                
                uuid = uuid_value   
                init_volume = leg[quote.VOLUME]                
 
                fields = [uuid, leg_id, symbol, otype, open_action, quantity, open_price,\
                        current_value, average_cost_basis, init_volume, status, trade_date,\
                        open_price, 0, trade_date, 0]

                sql = "INSERT INTO position ("+field_names+") VALUES("+values+")" 
                cursor = self.db_conn.cursor()          
                cursor.execute(sql, fields)
                msg = "BTO [%s|%s] [price:%.2f|q:%d] [%s|%s]" %\
                            (symbol, otype, strike, open_price, quantity, 
                             self.user.user_name, self.account_name)
                                
                self.create_transaction(leg, asset.BUY, asset.OPEN)
                continue

            open_action =leg[quote.OPEN_ACTION]
            quantity    =leg[pcl.SCALE] * q
            strike      =leg[quote.STRIKE]
            exp_date    =leg[quote.EXP_DATE]

            average_cost_basis = quantity * leg[quote.LAST_PRICE]
            if leg[quote.BID] > 0 and leg[quote.ASK] > 0:
                open_price = (leg[quote.BID] + leg[quote.ASK]) / 2
            else:
                open_price = leg[quote.LAST_PRICE]           

            average_cost_basis = 100* quantity * open_price
            current_value = average_cost_basis
            init_delta =  leg[quote.DELTA]
            init_IV =     leg[quote.IMPLIED_VOLATILITY]
            init_volume = leg[quote.VOLUME]
            init_open_interest = leg[quote.OPEN_INTEREST]
            status = asset.OPENED
            uuid = uuid_value            
            leg_id += 1
            fields = [uuid, leg_id, symbol, otype, strike, exp_date, open_action, quantity, open_price,\
                      current_value, average_cost_basis, init_delta, init_IV, init_volume,\
                      init_open_interest, status, trade_date,\
                      open_price, 0, trade_date, 0]
            
            sql = "INSERT INTO position ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)

            leg[pcl.QUANTITY]  = leg[pcl.SCALE] * q
            leg[pcl.OPEN_PRICE]  = leg[pcl.LAST_PRICE] = open_price  

            if open_action == asset.BUY_TO_OPEN:
                msg = "BTO [%s|%s|%s] [strike:%.2f|price:%.2f|q:%d] [%s|%s]" %\
                            (symbol, otype, exp_date, strike, open_price, quantity, 
                             self.user.user_name, self.account_name)

                self.create_transaction(leg, asset.BUY, asset.OPEN)
            elif open_action == asset.SELL_TO_OPEN:
                msg = "STO [%s|%s|%s] [strike:%.2f|price:%.2f|q:%d] [%s|%s]" %\
                        (symbol, otype, exp_date, strike, open_price, quantity,                
                        self.user.user_name, self.account_name)

                self.create_transaction(leg, asset.SELL, asset.OPEN)                
            else:
                self.logger.error("Invalie open_action %s" % open_action)
                raise Exception("Invalie open_action %s" % open_action)

            self.logger.debug(msg)

            legdesc.append(json.dumps(vars(self.optionLegDesc(exp_date, leg))))

        return  json.dumps(legdesc)
    
    def close_position(self, row):     
        symbol      = row[pcl.SYMBOL]  
        stock_price = get_price(symbol)                
        strike      = row[pcl.STRIKE]
        otype       = row[pcl.OTYPE]
        open_action = row[pcl.OPEN_ACTION]
        open_price  = row[pcl.OPEN_PRICE]
        quantity    = row[pcl.QUANTITY]
        exp_date    = row[pcl.EXP_DATE]

        if otype == asset.CALL:
            last_price = 0 if stock_price <= strike else stock_price - strike 
        elif otype == asset.PUT:
            last_price = 0 if stock_price >= strike else strike - stock_price
        else:
            self.logger.error("Invalie otype %s" % otype)
            return
        gain = (last_price - open_price) if open_action == asset.BUY_TO_OPEN else (open_price-last_price)
        total_gain_loss = gain * quantity  * 100
        total_gain_loss_percent = (gain / open_price) * 100                               
        current_value  = last_price * quantity * 100
                            
        sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                total_gain_loss_percent=?, status=? where leg_id ==? and uuid==?"""
        
        data = (last_price, current_value, total_gain_loss, total_gain_loss_percent, asset.CLOSED, row[pcl.LEG_ID], row[pcl.UUID])

        row[pcl.LAST_PRICE] = last_price
        if open_action == asset.BUY_TO_OPEN:
            msg = "[%s|%s] STC [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)            
            self.create_transaction(row, asset.SELL, asset.CLOSE)
        elif open_action == asset.SELL_TO_OPEN:
            msg = "[%s|%s] BTC [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)                                                                                   
            self.create_transaction(row, asset.BUY, asset.CLOSE)            
        else:
            self.logger.error("Invalie open_action %s" % open_action)
            raise Exception("Invalie open_action %s" % open_action)

        cursor = self.db_conn.cursor()       
        cursor.execute(sql, data)                    
        self.db_conn.commit()             
        self.logger.info(msg)
        return
    
    def expire_position(self, row):

        # covered call!!
        if row[pcl.OTYPE] == asset.STOCK:            
            return row[pcl.LAST_PRICE]
        
        exp_date = row[pcl.EXP_DATE]        
        symbol   = row[pcl.SYMBOL]
        data      = get_price_history(symbol, period='1mo')   
        exp_stock_price = data['Close'][pd.Timestamp(exp_date).tz_localize(data.index[-1].tz)]                     
        strike          = row[pcl.STRIKE]
        otype           = row[pcl.OTYPE]
        open_action     = row[pcl.OPEN_ACTION]
        quantity        = row[pcl.QUANTITY]
        today = datetime.now(timezone(app_settings.TIMEZONE))        
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")    

        if otype == asset.CALL:
            row[pcl.LAST_PRICE] = 0 if exp_stock_price <= strike else exp_stock_price - strike 
            if open_action == asset.BUY_TO_OPEN:
                gain = row[pcl.LAST_PRICE]  - row[pcl.OPEN_PRICE]
            else:
                gain = row[pcl.OPEN_PRICE]  - row[pcl.LAST_PRICE]
            row[pcl.TOTAL_GAIN_LOSS] = gain * row[pcl.QUANTITY]  * 100
            row[pcl.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[pcl.OPEN_PRICE]) * 100                
        elif otype == asset.PUT:
            row[pcl.LAST_PRICE] = 0 if exp_stock_price >= strike else strike - exp_stock_price
            if open_action == asset.BUY_TO_OPEN:
                gain = row[pcl.LAST_PRICE] - row[pcl.OPEN_PRICE]
            else:
                gain = row[pcl.OPEN_PRICE] - row[pcl.LAST_PRICE]                  
            row[pcl.TOTAL_GAIN_LOSS] = gain * row[pcl.QUANTITY]  * 100
            row[pcl.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[pcl.OPEN_PRICE]) * 100                 
        else:
            self.logger.error("Invalie otype %s" % otype)
            return
        
        row[pcl.CURRENT_VALUE]  = row[pcl.LAST_PRICE] * row[pcl.QUANTITY]  * 100
                            
        sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                total_gain_loss_percent=?, status=? ,last_quote_date=? where leg_id ==? and uuid==?"""
        
        data = (row[pcl.LAST_PRICE], row[pcl.CURRENT_VALUE],row[pcl.TOTAL_GAIN_LOSS],\
                row[pcl.TOTAL_GAIN_LOSS_PERCENT], asset.EXPIRED, last_quote_date, row[pcl.LEG_ID], row[pcl.UUID])

        if open_action == asset.BUY_TO_OPEN:
            msg = "[%s|%s] EXP L [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)            
            self.create_transaction(row, asset.SELL, asset.CLOSE)
        elif open_action == asset.SELL_TO_OPEN:
            msg = "[%s|%s] EXP S [%s|%s|%s|%.2f] [gain:%.2f|q:%d]" % (self.user.user_name, self.account_name,\
                        symbol, otype, exp_date, strike, gain, quantity)             
            self.create_transaction(row, asset.BUY, asset.CLOSE)            
        else:
            self.logger.error("Invalie open_action %s" % open_action)
            raise Exception("Invalie open_action %s" % open_action)

        cursor = self.db_conn.cursor()       
        cursor.execute(sql, data)                    
        self.db_conn.commit()             
        self.logger.info(msg)
        return row[pcl.LAST_PRICE]
    
    def update_position(self):

        #if afterHours():
        #    self.logger.warning('Cannot update position after hours!!')
        #    return []

        if 'IB' in self.brokerage:
            return self.update_ib_position()

        df = pd.read_sql_query("SELECT * FROM position WHERE status = '"+asset.OPENED+"'", self.db_conn)
        if df.shape[0] == 0:
            return []
               
        today = datetime.now(timezone(app_settings.TIMEZONE))
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")            
        symbol_list = df[pcl.SYMBOL].unique()            
        for symbol in symbol_list:
            stock_price = get_price(symbol)               
            sdf = df[df[pcl.SYMBOL]==symbol]
            for i, row in sdf.iterrows():         
                row[pcl.LAST_QUOTE_DATE] = last_quote_date                       
                otype = row[pcl.OTYPE]
                if otype == asset.STOCK:                    
                    row[pcl.LAST_PRICE] = stock_price
                    if row[pcl.OPEN_ACTION] == asset.BUY_TO_OPEN: 
                        gain = (row[pcl.LAST_PRICE] - row[pcl.OPEN_PRICE]) 
                        row[pcl.TOTAL_GAIN_LOSS] = gain * row[pcl.QUANTITY] * 100 
                        row[pcl.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[pcl.OPEN_PRICE]) * 100                
                    else:          
                        gain = (row[pcl.OPEN_PRICE] - row[pcl.LAST_PRICE])      
                        row[pcl.TOTAL_GAIN_LOSS] = gain * row[pcl.QUANTITY] 
                        row[pcl.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[pcl.OPEN_PRICE]) * 100                

                    row[pcl.CURRENT_VALUE] = row[pcl.LAST_PRICE] * row[pcl.QUANTITY] 

                    sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                        total_gain_loss_percent=?,last_quote_date=? where symbol ==? and trade_date==? and quantity==? and uuid==?"""
                    data = (row[pcl.LAST_PRICE], row[pcl.CURRENT_VALUE],row[pcl.TOTAL_GAIN_LOSS],\
                            row[pcl.TOTAL_GAIN_LOSS_PERCENT],row[pcl.LAST_QUOTE_DATE],\
                            row[pcl.SYMBOL], row[pcl.TRADE_DATE], row[pcl.QUANTITY], row[pcl.UUID])
                    cursor = self.db_conn.cursor()        
                    cursor.execute(sql, data)
                    self.db_conn.commit()                                                        
                elif otype in [asset.CALL, asset.PUT]:
                    exp_date = row[pcl.EXP_DATE]
                    days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days+1                           
                    if days_to_expire < 0:
                        self.expire_position(row)
                        continue                  
                               
                    strike = row[quote.STRIKE]
                    op = get_option_leg_details(symbol, stock_price, exp_date, strike, otype)
                    if len(op) == 0:
                        self.logger.error('Cannot find quote for option leg %s %s %s %s' % (symbol, otype, str(strike), str(exp_date)))
                        continue
            
                    row[pcl.LAST_PRICE] = (op[quote.BID]+op[quote.ASK]) / 2  if  (op[quote.BID]+op[quote.ASK]) > 0 else  op[quote.LAST_PRICE]                 
                        
                    row[pcl.CURRENT_VALUE] = row[pcl.LAST_PRICE] * row[pcl.QUANTITY] * 100

                    if row[pcl.OPEN_ACTION] == asset.BUY_TO_OPEN: 
                        gain = (row[pcl.LAST_PRICE] - row[pcl.OPEN_PRICE]) 
                        row[pcl.TOTAL_GAIN_LOSS] = gain * row[pcl.QUANTITY] * 100 
                        row[pcl.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[pcl.OPEN_PRICE]) * 100                
                    else:          
                        gain = (row[pcl.OPEN_PRICE] - row[pcl.LAST_PRICE])      
                        row[pcl.TOTAL_GAIN_LOSS] = gain * row[pcl.QUANTITY] 
                        row[pcl.TOTAL_GAIN_LOSS_PERCENT] = (gain / row[pcl.OPEN_PRICE]) * 100                
                       
                    row[pcl.LAST_DELTA] = op[quote.DELTA]
                    row[pcl.LAST_IV]    = op[quote.IMPLIED_VOLATILITY]
                    row[pcl.LAST_OPEN_INTEREST] = op[quote.OPEN_INTEREST]   
                    row[pcl.LAST_VOLUME] = op[quote.VOLUME]               

                    sql = """update position set last_price=?, current_value=?, total_gain_loss=?,\
                        total_gain_loss_percent=?,last_delta=?,last_IV=?,last_open_interest=?,last_volume=?,\
                        last_quote_date=? where leg_id ==? and uuid==?"""
                    
                    data = (row[pcl.LAST_PRICE], row[pcl.CURRENT_VALUE],row[pcl.TOTAL_GAIN_LOSS],\
                            row[pcl.TOTAL_GAIN_LOSS_PERCENT],row[pcl.LAST_DELTA],row[pcl.LAST_IV],\
                            row[pcl.LAST_OPEN_INTEREST], row[pcl.LAST_VOLUME], row[pcl.LAST_QUOTE_DATE],\
                            row[pcl.LEG_ID],row[pcl.UUID])
                    
                    cursor = self.db_conn.cursor()        
                    cursor.execute(sql, data)                    
                    self.db_conn.commit()     
                else:
                    self.logger.error('Unahndled %s type position' % otype)          

        return self.update_position_summary()
 
    def create_position_summary(self, row):
        uuid_value = UUID.uuid4().hex
        symbol =       row[pscl.SYMBOL]
        exp_date =     row[pscl.EXP_DATE]
        strategy =     row[pscl.STRATEGY]
        quantity =     row[pscl.QUANTITY]
        open_price =   row[pscl.OPEN_PRICE] 
        breakeven_l =  row[pscl.BREAKEVEN_L]
        breakeven_h =  row[pscl.BREAKEVEN_H]
        max_profit =   row[pscl.MAX_PROFIT]
        max_loss =     row[pscl.MAX_LOSS]
        pnl =          row[pscl.PNL]
        win_prob =     row[pscl.WIN_PROB]
        credit = str(True) if row[pscl.MARGIN] > 0 else str(False) 
        trade_date =  str(row[pscl.TRADE_DATE])
        trade_stock_price = row[pscl.TRADE_STOCK_PRICE]   
        spread =       row[pscl.SPREAD]         
        target_low  = row[pscl.TARGET_LOW]
        target_high = row[pscl.TARGET_HIGH]

        legs =        row[pscl.LEGS]    

        # if json string
        if isinstance(legs , str):         
            legs_desc = legs            
            leg_list = json.loads(legs)
            legs = []
            for l in leg_list:
                lo = json.loads(l)
                lo[quote.LAST_PRICE] = lo['price']
                lo[quote.BID] = lo[quote.ASK] = 0
                lo[quote.SYMBOL] = symbol
                legs.append(lo)
            row[pscl.LEGS] = legs
        else:
            legdesc = []
            for leg in legs:
                legdesc.append(json.dumps(vars(self.optionLegDesc(exp_date, leg))))
            legs_desc =  json.dumps(legdesc)
                               
        uuid = uuid_value        

        df = self.user.site.get_monitor_df(filter=[symbol])
        if df.shape[0] == 1:
            earning_date = df.head(1)['earning'].values[0]
        else:
            try:
                earning_date = get_next_earning_date(symbol)
                earning_date = "" if earning_date == None else str(earning_date)
            except Exception as ex:
                self.logger.exception(ex)
                earning_date = "" 

        cash_position = self.get_BuyingPower()
        margin_position = self.get_margin_position()          
        if math.isnan(margin_position):
             margin_position = 0.0

        if math.isnan(row[pscl.MARGIN]):
            margin=0.0
        else:
            margin = quantity * 100 * row[pscl.MARGIN]
        
        cash = quantity * 100 * row[pscl.OPEN_PRICE]   
        last_price = open_price
        pl = 0.0
        gain=0.0
        last_quote_date = trade_date
        last_stock_price = trade_stock_price
        last_win_prob = win_prob
                       
        fields = [uuid, symbol, strategy, credit, spread, open_price, exp_date, breakeven_l,breakeven_h,\
                  max_profit,max_loss,pnl, win_prob,trade_date,earning_date,trade_stock_price,\
                  margin,quantity,legs_desc, target_low, target_high, cash, margin, cash_position,\
                  margin_position,\
                  last_price, pl, gain, last_quote_date, last_stock_price, last_win_prob]

        field_names =  "uuid,symbol,strategy,credit,spread,open_price,exp_date,\
                        breakeven_l,breakeven_h,max_profit,max_loss,pnl,win_prob,trade_date,\
                        earning_date,trade_stock_price,margin,quantity,legs_desc, target_low, target_high,\
                        open_cash, open_margin, cash_position, margin_position,\
                        last_price, pl, gain, last_quote_date, last_stock_price, last_win_prob"        

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'                      

        if 'IB' in self.brokerage:
            live = False if 'PAPER' in self.brokerage else True
            x = place_ib_order(row, TWS=ib_settings.TWS, live=live, bracket=False)
            if len(x.ib_errorString) > 0:
                msg = "CREATE IB_ORDER FAILED %s errodCode %s [%s|%s|%s] [pri:%.2f|pnl:%.2f|prob:%.2f|q:%d] %s [%s]" %\
                    (x.ib_errorString, str(x.ib_errorCode), strategy, symbol, exp_date, open_price,
                    pnl, win_prob, quantity, self.print_legs(legs_desc),self.account_name)
                self.logger.error(msg)        
                field_names += ", ib_errorString, ib_errorCode, ib_advancedOrderRejectJson"
                fields += [x.ib_errorString, 
                           x.ib_errorCode, 
                           x.ib_advancedOrderRejectJson]            
                values +=",?,?,?"             
                status = asset.OPEN_FAILED               
            else:
                field_names += ", ib_clientId, ib_orderId, ib_status, ib_permId, ib_parentId, ib_clientId, ib_filled, ib_remaining, ib_avgFillPrice, ib_lastFillPrice, ib_whyHeld, ib_mktCapPrice, ib_tif"
                fields += [x.ib_clientId, 
                        x.ib_orderId, 
                        x.ib_status, 
                        x.ib_permId, 
                        x.ib_parentId, 
                        x.ib_clientId, 
                        x.ib_filled, 
                        x.ib_remaining, 
                        x.ib_avgFillPrice, 
                        x.ib_lastFillPrice, 
                        x.ib_whyHeld, 
                        x.ib_mktCapPrice, 
                        x.ib_tif]
                values +=",?,?,?,?,?,?,?,?,?,?,?,?,?"
                status = asset.OPEN_PENDING                
        else:
            status = asset.OPENED

        field_names += ", status"
        fields += [status]
        values += ',?'

        sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        
        if 'IB' in self.brokerage:
            self.db_conn.commit()              
            if status == asset.OPEN_PENDING:
                msg = "CREATE PENDING [%s|%s|%s] [pri:%.2f|pnl:%.2f|prob:%.2f|q:%d] %s [%s]" %\
                    (strategy, symbol, exp_date, open_price, pnl, 
                    win_prob, quantity, self.print_legs(legs_desc),self.account_name)

            if status == asset.OPEN_FAILED:
                msg = "CREATE FAILED [%s|%s|%s] [pri:%.2f|pnl:%.2f|prob:%.2f|q:%d] %s [%s] %s %s" %\
                    (strategy, symbol, exp_date, open_price, pnl, 
                    win_prob, quantity, self.print_legs(legs_desc),self.account_name,
                    x.ib_errorString, str(x.ib_errorCode))           

            return msg
        
        self.create_position(symbol, legs, quantity, uuid_value, trade_date)   

        if credit == 'True':        
            margin_position += margin
            cash_position += (cash-margin)            
            self.__update_margin_position(margin_position, commit=False)        
        else:
            cash_position -= cash

        self.__update_cash_position(cash_position, commit=False)  

        self.db_conn.commit()    

        msg = "CREATE [%s|%s|%s] [pri:%.2f|pnl:%.2f|prob:%.2f|q:%d] %s [%s]" %\
              (strategy, symbol, exp_date, open_price, pnl, 
               win_prob, quantity, self.print_legs(legs_desc),self.account_name)

        self.logger.info(msg)
        return msg
                           
    def expire_position_summary(self, srow):

        today = datetime.now(timezone(app_settings.TIMEZONE))
        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")   
                
        uuid = srow[pscl.UUID]

        pdf= pd.read_sql_query("SELECT * FROM position WHERE uuid = '"+uuid+"'", self.db_conn)

        stock_prow = None
        last_price = 0
        for i, prow in pdf.iterrows(): 
            if prow[pcl.OTYPE] == asset.STOCK:
                stock_prow = prow
                continue
    
            if prow[pcl.STATUS] == asset.OPENED:
                exp_price = self.expire_position(prow)
            else:                
                exp_price = prow[pcl.LAST_PRICE] 

            if prow[pcl.OPEN_ACTION] == asset.BUY_TO_OPEN:
                last_price -= exp_price
            else:
                last_price += exp_price     

        exp_date = srow[pscl.EXP_DATE]        
        symbol   = srow[pscl.SYMBOL]
        data = get_price_history(symbol, period='1mo')        
        strategy = srow[pscl.STRATEGY]
        exp_stock_price = data['Close'][pd.Timestamp(exp_date).tz_localize(data.index[-1].tz)]        
        open_price = srow[pscl.OPEN_PRICE] 
        credit = srow[pscl.CREDIT]=='True'
        quantity = srow[pscl.QUANTITY]
        stop_date = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")
        stop_reason = asset.EXPIRED
        exp_price = stop_price = last_price
        gain = open_price-last_price if credit else last_price-open_price
        pl = gain * quantity * 100
        gain = 100 * (gain / open_price)
        cash = pl
        legs = srow[pscl.LEGS]
        if credit:             
            margin = srow[pscl.MARGIN]      
            margin_position = self.get_margin_position() - margin
            cash += margin
            self.__update_margin_position(margin_position, False)  
        else:
            margin_position = self.get_margin_position()             
            margin=0

        cash_position = self.get_BuyingPower() 
        cash_position += cash
        self.__update_cash_position(cash_position, False)                

        sql = """update position_summary set exp_stock_price=?, exp_price=?, last_price=?, pl=?, gain=?, status=?, stop_date=?, stop_reason=?, stop_price=?,last_quote_date=?, close_cash=?, close_margin=?, cash_position=?, margin_position=? where uuid==?"""        
        data = (exp_stock_price, exp_price, last_price, pl, gain, asset.EXPIRED, stop_date, stop_reason, stop_price,  last_quote_date, cash, margin, cash_position, margin_position,uuid)
        cursor = self.db_conn.cursor()    
        cursor.execute(sql, data)     
        
        msg = "EXPIRE  [%s|%s|%s] [prof:%.2f|gain:%.2f|q:%d] [cash:%.2f|margin:%.2f][cash_position:%.2f|margin_position%.2f] %s [%s] " %\
                        (strategy, symbol,exp_date, pl, gain, quantity, pl, margin, cash_position, margin_position,
                         self.print_legs(legs),self.account_name)

        self.logger.info(msg)                

        #lineNotifyMessage( msg, token=self.user.notification_token)    

        if strategy == st.COVERED_CALL:
            self.expire_covered_call_post_process(stock_prow, exp_date, exp_stock_price)

        self.db_conn.commit()    

        return msg
    
    def roll_position_summary(self, symbol, exp_date, strategy):

        today = datetime.now(timezone(app_settings.TIMEZONE))

        earning_date = get_next_earning_date(symbol)
        if earning_date is not None:
            days_to_earning = (earning_date - today).days               
            if days_to_earning <= self.risk_mgr.close_days_before_expire:
                return ""  

        cash = self.get_BuyingPower()
        init_balance = self.get_initial_balance()
        cash_ratio = 100 * cash/init_balance
        if cash_ratio < self.risk_mgr.min_cash_percent:
            self.logger.warning('Cash ratio %.2f lower than setting %2f' % (cash_ratio, self.risk_mgr.min_cash_percent))
            return ""

        acct_value = self.get_account_value()    
        if acct_value == 0:
            return ""
            
        risk_matrix = self.get_risk_matrix()
        risk_ratio = risk_matrix[pscl.MAX_RISK]/acct_value 
        if risk_ratio  >=  app_settings.RISK_MGR.max_risk_ratio/100:
            self.logger.warning('Risk ratio %.2f higher than setting %2f' % (risk_ratio, self.risk_mgr.max_risk_ratio))
            return ""

        exp_date_list = [exp_date]

        if strategy   == st.LONG_CALL:
            df = self.roll_option_long( symbol, exp_date_list, asset.CALL)                
        elif strategy == st.LONG_PUT:
            df = self.roll_option_long( symbol, exp_date_list, asset.PUT)
        elif strategy == st.COVERED_CALL:
            df = self.roll_option_short(symbol, exp_date_list, asset.CALL)     
        elif strategy == st.SHORT_PUT:
            df = self.roll_option_short( symbol, exp_date_list, asset.PUT)                       
        elif strategy == st.CREDIT_CALL_SPREAD:
            df = self.roll_vertical_call_spread( symbol, exp_date_list,  credit=True)            
        elif strategy == st.DEBIT_CALL_SPREAD:
            df = self.roll_vertical_call_spread( symbol, exp_date_list, credit=False)                                       
        elif strategy==  st.CREDIT_PUT_SPREAD:
            df = self.roll_vertical_put_spread( symbol, exp_date_list,  credit=True)                     
        elif strategy == st.DEBIT_PUT_SPREAD:
            df = self.roll_vertical_put_spread( symbol, exp_date_list, credit=False)                    
        elif strategy==  st.CREDIT_IRON_CONDOR:
            df = self.roll_iron_condor( symbol, exp_date_list, credit=True)
        elif strategy == st.DEBIT_IRON_CONDOR:
            df = self.roll_iron_condor( symbol, exp_date_list, credit=False)                    
        elif strategy == st.CREDIT_PUT_BUTTERFLY:
            df = self.roll_put_butterfly(symbol, exp_date_list, credit=True)                                              
        elif strategy == st.CREDIT_CALL_BUTTERFLY:
            df = self.roll_call_butterfly( symbol, exp_date_list, credit=True)                                               
        elif strategy == st.DEBIT_PUT_BUTTERFLY:
            df = self.roll_put_butterfly( symbol, exp_date_list, credit=False)                 
        elif strategy == st.DEBIT_CALL_BUTTERFLY:
            df = self.roll_call_butterfly( symbol, exp_date_list, credit=False)      
        elif strategy == st.IRON_BUTTERFLY:
            df = self.roll_iron_butterfly( symbol, exp_date_list, credit=True)                          
        elif strategy == st.REVERSE_IRON_BUTTERFLY:
            df = self.roll_iron_butterfly( symbol, exp_date_list, credit=False)                   
        elif strategy == st.WEEKLY_STOCK_TRADE:
            # don't roll 
            return
        else:
            self.logger.error('Unsupported strategy %s' % strategy)
            return ""
                    
        if df.shape[0] == 0:
            return ""
        
        df.sort_values(by = [pscl.WIN_PROB, pscl.PNL], ascending=False, inplace=True)                                          

        opt = df.head(1).to_dict('records')[0]     

        q = self.risk_mgr.max_loss_per_position // (opt[pscl.MAX_LOSS] * 100)
        if q == 0:
            self.logger.debug('max loss %.2f exceeded max per position risk %.2f' % (opt[pscl.MAX_LOSS] * 100, self.risk_mgr.max_loss_per_position))
            return ""

        opt[pscl.QUANTITY] = q

        opt[pscl.MAX_RISK] = opt[pscl.MAX_LOSS] * opt[pscl.QUANTITY] if opt[pscl.STRATEGY] != st.UNPAIRED else opt[pscl.OPEN_PRICE]

        symbol_risk_list = risk_matrix[pscl.SYMBOL]

        exp_date_risk_list = risk_matrix[pscl.EXP_DATE]

        symbol_risk = symbol_risk_list[symbol] if symbol in symbol_risk_list else 0.0
        if symbol_risk + opt[pscl.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_asset /100:
            return ""

        exp_risk = exp_date_risk_list[exp_date] if exp_date in exp_date_risk_list else 0.0
        if exp_risk + opt[pscl.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_expiration_date / 100:
            return ""
        
        return self.create_position_summary(opt)  
        
    def update_position_summary(self):
          
        today = datetime.now(timezone(app_settings.TIMEZONE))

        last_quote_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")   
        
        sdf = pd.read_sql_query("SELECT * FROM position_summary WHERE status = '"+asset.OPENED+"'", self.db_conn)

        uuid_list = sdf[pscl.UUID].unique()      

        trade_rec_list = []

        for uuid in uuid_list:       
            
            if uuid == None:
                continue

            srow = sdf[sdf[pscl.UUID]==uuid].iloc[0]
            symbol = srow[pscl.SYMBOL]
            stock_price = get_price(symbol)        
            strategy = srow[pscl.STRATEGY]
            if strategy == st.UNPAIRED:
                open_price = srow[pscl.OPEN_PRICE]
                last_price = stock_price
                credit = srow[pscl.CREDIT]=='True'
                quantity = srow[pscl.QUANTITY]

                gain = open_price - last_price if credit else last_price - open_price            
                pl = gain * quantity
                gain = 100 * (gain / open_price)

                r = self.user.site.get_monitor_rec(symbol)
                if len(r) > 0:
                    target_low  = r['target_low']
                    target_high = r['target_high']
                else:
                    target_low = target_high = np.nan

                # quartly return target
                breakeven_l = last_price +  (last_price * app_settings.TARGET_ANNUAL_RETURN / 100)
                today = datetime.now(timezone(app_settings.TIMEZONE))        
                from dateutil.relativedelta import relativedelta        
                three_mon_rel = relativedelta(months=12)
                target_date = str((today + three_mon_rel).date()) 
                last_win_prob = calc_win_prob(symbol, target_date, st.UNPAIRED, breakeven_l, np.nan)
        
                sql = """update position_summary set last_price=?, pl=?, gain=?, last_quote_date=?, last_stock_price=?, target_low=?, target_high=?, breakeven_l=?, last_win_prob=? where uuid==?"""        
                data = (last_price, pl, gain, last_quote_date, last_price, target_low, target_high, breakeven_l, last_win_prob, uuid)                                
                cursor = self.db_conn.cursor()    
                cursor.execute(sql, data) 
                self.db_conn.commit()   
                continue
        
            exp_date = srow[pscl.EXP_DATE]
            trade_date = str(srow[pscl.TRADE_DATE])            

            try:
                days_open = (today-pd.Timestamp(trade_date).tz_convert(timezone(app_settings.TIMEZONE))).days+1
            except Exception as ex:
                days_open = (today-pd.Timestamp(trade_date).tz_localize(timezone(app_settings.TIMEZONE))).days+1
                pass

            days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days+1                      
            if days_to_expire < 0:  
                self.expire_position_summary(srow)
                continue

            ppdf = pd.read_sql_query("SELECT * FROM position WHERE uuid = '"+uuid+"'", self.db_conn)

            quantity = srow[pscl.QUANTITY]            

            last_price = 0

            for i, prow in ppdf.iterrows():
                
                if prow[pcl.OTYPE] == asset.STOCK: #covered call
                    continue

                if prow[pcl.LAST_PRICE] == None: #canot get quote, give up update
                    last_price = 0
                    break

                scale = prow[pcl.QUANTITY] / quantity 
                if prow[pcl.OPEN_ACTION] == asset.BUY_TO_OPEN:
                    last_price -= (scale * prow[pcl.LAST_PRICE])
                else:
                    last_price += (scale * prow[pcl.LAST_PRICE])

            credit = srow[pscl.CREDIT] == 'True'

            if (credit) and (last_price <= 0):
                continue
            
            if (credit == False) and (last_price >= 0):
                continue

            last_price = abs(last_price)
            
            win_prob = calc_win_prob(symbol, exp_date, strategy, srow[pscl.BREAKEVEN_L], srow[pscl.BREAKEVEN_H])

            open_price = abs(srow[pscl.OPEN_PRICE]) 
            credit = srow[pscl.CREDIT]=='True'
            quantity = srow[pscl.QUANTITY]
            legs = srow[pscl.LEGS]

            gain = open_price - last_price if credit else last_price - open_price            
            pl = gain * quantity * 100
            gain = 100 * (gain / open_price)
            sql = """update position_summary set last_price=?, pl=?, gain=?, last_quote_date=?, last_stock_price=?, last_win_prob=? where uuid==?"""        
            data = (last_price, pl, gain, last_quote_date, stock_price, win_prob, uuid)
            cursor = self.db_conn.cursor()    
            cursor.execute(sql, data)     
            self.db_conn.commit()  

            stopped = False
            roll = False
            if gain >= self.risk_mgr.stop_gain_percent:
                stopped = True
                stop_reason = 'Stop Gain %.2f >= %.2f'% (gain, self.risk_mgr.stop_gain_percent)            
                if days_to_expire > 5:
                    roll = True
            elif gain < 0 and abs(gain) >= self.risk_mgr.stop_loss_percent:
                stopped = True            
                stop_reason =  'Stop Loss %.2f >= %.2f'  % (gain, self.risk_mgr.stop_loss_percent)    
                if days_to_expire > 5:
                    roll = True
            elif days_to_expire <= self.risk_mgr.close_days_before_expire:
                stopped = True   
                stop_reason = 'Days to expire %d <= %d' % (days_to_expire, self.risk_mgr.close_days_before_expire)            
            elif win_prob < 10:
                stopped = True   
                stop_reason = 'Last Win Prob %.2f <= 10' % (win_prob)                          
            else:
                try:
                    datetime.fromisoformat(srow[pscl.EARNING_DATE])
                    earning_date = pd.Timestamp(srow[pscl.EARNING_DATE]).tz_convert(timezone(app_settings.TIMEZONE))                 
                    days_to_earning = (earning_date - today).days+1               
                    if days_to_earning <= self.risk_mgr.close_days_before_expire:
                        stopped = True                           
                        stop_reason = 'Days to earning %d <= %d'  % (days_to_earning, self.risk_mgr.close_days_before_expire)    
                except ValueError:
                     pass                   
                                             
            if stopped:              

                if afterHours() or self.runtime_config.auto_trade == False:
                    msg = "STOP PENDING  [%s|%s|%s] [days opened %d|reason:%s|pl:%.2f|gain:%.2f|q:%d] %s [%s]" %\
                            (strategy, symbol,exp_date, days_open,stop_reason,
                             pl, gain, quantity, self.print_legs(legs),self.account_name)
                    self.logger.info(msg)             
                    #lineNotifyMessage( msg, token=self.user.notification_token)   

                    trade_rec_list.append(msg)                    
                else:

                    for i, prow in ppdf.iterrows():
                        self.close_position(prow)

                    if credit:             
                        margin =  srow[pscl.MARGIN]      
                        margin_position = self.get_margin_position() - margin
                        cash = pl+margin
                        self.__update_margin_position(margin_position, commit=False)  
                    else:
                        cash = pl
                        margin_position = self.get_margin_position()                         
                        margin=0
                    cash_position = self.get_BuyingPower() + cash  
                    self.__update_cash_position(cash_position, commit=False) 
                    last_quote_date = stop_date = today.strftime("%Y-%m-%d %H:%M:%S %Z")
                    sql = """update position_summary set last_price=?, pl=?, gain=?, last_quote_date=?, stop_date=?, stop_reason=?, status=?, last_stock_price=?, close_cash=?, close_margin=?, cash_position=?, margin_position=? where uuid==?"""        
                    data = (last_price, pl, gain, last_quote_date, stop_date, stop_reason, asset.CLOSED, stock_price, cash, margin, cash_position, margin_position, uuid)                                
                    cursor = self.db_conn.cursor()    
                    cursor.execute(sql, data)     
                    self.db_conn.commit()   
                    msg = "STOP  [%s|%s|%s] [open days %d|reason:%s|pl:%.2f|gain:%.2f|q:%d] [cash:%.2f|margin:%.2f][cash_position:%.2f|margin_position%.2f] %s [%s]" %\
                             (strategy, symbol, exp_date, days_open, stop_reason, pl, gain, quantity, pl, margin, cash_position, margin_position, 
                              self.print_legs(legs),self.account_name)   
                    
                    self.logger.info(msg)             
                    #lineNotifyMessage( msg, token=self.user.notification_token)            

                    trade_rec_list.append(msg)

                    roll_msg = ''
                    #if roll:            
                    #    roll_msg_list = self.roll_position_summary(symbol, exp_date, strategy)                    
                    #    trade_rec_list += roll_msg_list

        return trade_rec_list

    def print_legs(self, leg_list):
        output_str = ''
    
        legs = json.loads(leg_list)

        for leg in legs:
            ld = json.loads(leg)
            if 'otype' in ld:
                leg_desc = ' [%s|%s|%.2f|%.2f|%d|%s] ' % (ld[pcl.OPEN_ACTION], ld[pcl.OTYPE], ld[pcl.STRIKE], ld['price'], ld[pcl.SCALE], ld[pcl.EXP_DATE])
            else: # delete in future
                leg_desc = ' [%s|%s|%.2f|%.2f|%d|%s] ' % (ld['OPEN_ACTION'], ld['OTYPE'], ld['STRIKE'], ld['PRICE'], ld['QUANTITY'], ld['EXP_DATE'])                
            output_str += leg_desc
        return output_str
    
    def get_position_summary(self, status=[], get_leg_dedail=False):    

        if app_settings.DATABASES == 'sqlite3':             

            df = pd.read_sql_query("SELECT * FROM position_summary", self.db_conn)   

            if len(status) > 0:
                df = df[df[pscl.STATUS].isin(status)]

            if get_leg_dedail:
                for i, row in df.iterrows():                    
                    if row[pscl.LEGS] == None:
                        continue

                    index = 0                
                    legs = json.loads(row[pscl.LEGS])    
                    for leg in legs:
                        index += 1                
                        leg_desc = json.loads(leg)
                        if 'OTYPE' in leg_desc: # legacy data, need clean up
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.OTYPE]              = leg_desc['OTYPE']
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.STRIKE]             = leg_desc['STRIKE']
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.EXP_DATE]           = leg_desc['EXP_DATE']
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.OPEN_ACTION]        = leg_desc['OPEN_ACTION']
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.QUANTITY]           = leg_desc['QUANTITY']                                       
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.OPEN_PRICE]         = leg_desc['PRICE']                             
                            if 'IV' in leg_desc:
                                df.at[i, 'leg '+ str(index) + ' ' + pcl.INIT_IV]            = leg_desc['IV']                                                                                     
                                df.at[i, 'leg '+ str(index) + ' ' + pcl.INIT_DELTA]         = leg_desc['DELTA']            
                                df.at[i, 'leg '+ str(index) + ' ' + pcl.INIT_OPEN_INTEREST] = leg_desc['OPEN_INTEREST'] 
                        else:
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.OTYPE]              = leg_desc[pcl.OTYPE]
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.STRIKE]             = leg_desc[pcl.STRIKE]
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.EXP_DATE]           = leg_desc[pcl.EXP_DATE]
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.OPEN_ACTION]        = leg_desc[pcl.OPEN_ACTION]
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.SCALE]              = leg_desc[pcl.SCALE]                                       
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.OPEN_PRICE]         = leg_desc['price']                             
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.INIT_IV]            = leg_desc['impliedVolatility']                                                                                     
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.INIT_DELTA]         = leg_desc['delta']            
                            df.at[i, 'leg '+ str(index) + ' ' + pcl.INIT_OPEN_INTEREST] = leg_desc['openInterest'] 
            return df
        
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)    
            return pd.DataFrame()
        
    def get_account_profile(self):
        if app_settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM account_profile", self.db_conn)   
            return df         
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)    
            return pd.DataFrame()
           
    def update_account_profile(self, df):
        if app_settings.DATABASES == 'sqlite3':             
            df.to_sql('account_profile', self.db_conn, if_exists='replace', index=False)            
            return df         
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)    
            return pd.DataFrame()
                   
    def get_positions(self):    
        if app_settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM position", self.db_conn)   
            return df            
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)    
            return pd.DataFrame()
                     
    def get_transactions(self):   
        if app_settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM transactions", self.db_conn)   
            return df
        else:
            self.logger.error('Unsupported database engine %s' % app_settings.DATABASES)    
            return pd.DataFrame()        

    def weekly_stock_play(self):
        
        from option_trader.entity.monitor import cname

        if app_settings.DATABASES == 'sqlite3':              

            today = datetime.now(timezone(app_settings.TIMEZONE))

            ps = self.get_position_summary(status=[asset.OPENED])
            ps = ps[ps[pscl.STRATEGY]==st.UNPAIRED]

            if ps.shape[0] > 0:
                last_trade_date = self.get_position_summary(status=[asset.OPENED]).tail(1)[pscl.TRADE_DATE].values[0]
                days_to_last_trade = (today-pd.Timestamp(last_trade_date).tz_localize(timezone(app_settings.TIMEZONE))).days                           
                if days_to_last_trade < 5:
                    self.logger.debug("Days to last trade %d < 5" % days_to_last_trade)
                    return []
            
            amount = self.risk_mgr.weekly_stock_trade_amount                       
            min_cash_percent = self.risk_mgr.min_cash_percent #weekly_stock_trade_stop_percent
            buyingPower = self.get_BuyingPower() - amount
            account_value = self.get_account_value()
            if buyingPower < (min_cash_percent/ 100)  * account_value:
                self.logger.info('Buying Power lower than %.2f %% of account value %.2f' % ( min_cash_percent, account_value)) 
                return []     

            watchlist = self.get_default_watchlist()
            if len(watchlist) == 0:
                self.logger.info('Empty watchlist!!') 
                return []
                           
            candidates = self.user.site.get_monitor_df(filter=watchlist)[[cname.symbol,cname.ten_days_gain]]
            candidates.sort_values(cname.ten_days_gain, inplace=True)
            symbol = candidates.head(1).symbol.values[0]
            
            trade_rec = self.create_stockSummary(symbol)  
            
        return trade_rec

    def get_stock_open_shares(self, symbol):
        if self.brokerage == 'IB':
            pos = self.get_ib_account_portfolio()
            if pos.shape[0] == 0:
                return 0.0
            pos = pos[ (pos['symbol']==symbol) & (pos['secType']=='STK')]
            return pos['position'].sum() if pos.shape[0] > 0 else 0.0
        
        pos = self.get_position_summary(status=[asset.OPENED])
        if pos.shape[0] == 0:
            return 0.0
        
        pos = pos[(pos[pscl.SYMBOL]==symbol) & (pos[pscl.STRATEGY]==st.UNPAIRED)]
        if pos.shape[0] > 0:
            shares = pos[pcl.QUANTITY].sum()
            return shares
        else:
            return 0.0

    def get_account_history(self):
        if app_settings.DATABASES == 'sqlite3':             
            df = pd.read_sql_query("SELECT * FROM account_daily_summary", self.db_conn)   
            return df
        
    def create_daily_account_summary(self): 

        record_date = str(datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date())         

        s = self.get_account_summary()

        field_names =   "'Initial Balance', 'Acct Value', 'Asset Value','Cash','Margin',\
                        'Unrealized PL','Realized PL', 'Risk Ratio','Max Risk', 'Gain',\
                        'Trx # (all)', 'Win Rate (all)','Avg Loss (all)', 'Avg Win (all)','Trx# (opened)',\
                        'Win Rate (opened)', 'Avg Loss (opened)', 'Avg Win (opened)','Trx# (closed)','Win Rate (closed)',\
                        'Avg Win (closed)', 'Avg Loss (closed)', 'record date'"

        values =  '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?' 

        cl = summary_col_name

        fields = [s[cl.INIT_BALANCE], s[cl.ACCT_VALUE], s[cl.ASSET_VALUE], s[cl.CASH], s[cl.MARGIN],\
                  s[cl.UNREALIZED_PL], s[cl.REALIZED_PL], s[cl.RISK_RATIO], s[cl.MAX_RISK], s[cl.GAIN],\
                  s[cl.ALL_TRX_CNT], s[cl.ALL_WIN_RATE], s[cl.AVG_ALL_TRX_LOSS_PL], s[cl.AVG_CLOSED_TRX_WIN_PL], s[cl.OPENED_TRX_CNT],\
                  s[cl.OPENED_WIN_RATE], s[cl.AVG_OPENED_TRX_LOSS_PL], s[cl.AVG_OPENED_TRX_WIN_PL], s[cl.CLOSED_TRX_CNT],s[cl.CLOSED_WIN_RATE],\
                  s[cl.AVG_CLOSED_TRX_WIN_PL], s[cl.AVG_CLOSED_TRX_LOSS_PL], record_date]  
        
        sql = "INSERT OR REPLACE INTO  account_daily_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        self.db_conn.commit()    

        return pd.DataFrame([s])
    
    def expire_covered_call_post_process(self, spos, exp_date, last_stock_price):
        
        symbol = spos[pcl.SYMBOL]
        
        uuid = spos[pcl.UUID] + '||' + UUID.uuid4().hex

        trade_date = spos[pcl.TRADE_DATE] 
        status = asset.OPENED           
        trade_stock_price  = open_price = spos[pcl.OPEN_PRICE]    
                         
        earning_date = get_next_earning_date(symbol)
        earning_date = "" if earning_date == None else str(earning_date)
        credit =  str(False)
        strategy = st.UNPAIRED                    
        cash = 0.0
        margin = 0.0

        cash_position = self.get_BuyingPower()
        margin_position = self.get_margin_position()
        quantity =  spos[pcl.QUANTITY]        
        pl = (last_stock_price-open_price) * quantity 
        gain = 100 * (last_stock_price-open_price)/open_price 
        last_quote_date =exp_date        

        fields = [ uuid, symbol, strategy, credit, open_price,\
                  trade_date,earning_date,trade_stock_price,quantity,status,\
                  cash, margin, cash_position, margin_position,\
                  last_stock_price, pl, gain, last_quote_date, last_stock_price]

        field_names =  "uuid,symbol,strategy,credit,open_price,\
                        trade_date,earning_date,trade_stock_price,quantity,status,\
                        open_cash, open_margin, cash_position, margin_position,\
                        last_price, pl, gain, last_quote_date, last_stock_price"
        
        values = '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'

        sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        msg = "Unpaired Expired Covered Call Stock Position %s [price:%.2f|quantity:%d] %s" %\
             (symbol, open_price, quantity,self.account_name)
        self.logger.info(msg)   
        return msg

    def create_stockSummary(self, symbol):
        
        amount = self.risk_mgr.weekly_stock_trade_amount      
        quote = get_price_history(symbol, period='1d', interval='1d')
        price = quote['Close'][-1]
        quantity = round(amount / price, 2)

        if afterHours() or self.runtime_config.auto_trade == False:
            msg = "BUY PENDING %s [price:%.2f|quantity:%.2f] %s" % (symbol,price,quantity,self.account_name)
            self.logger.info(msg)
            return msg

        uuid = UUID.uuid4().hex
        trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date() 
        open_action =asset.BUY_TO_OPEN                       
        volume = float(quote['Volume'][-1])
        open_price = price           
        average_cost_basis = quantity * price                 
        current_value = average_cost_basis                          
        otype = asset.STOCK
        open_action = asset.BUY_TO_OPEN        
        leg_id = 0

        r = self.user.site.get_monitor_rec(symbol)
        target_low  = r['target_low']
        target_high = r['target_high']
                
        breakeven_l = open_price +  (open_price * app_settings.TARGET_ANNUAL_RETURN / 100)
        today = datetime.now(timezone(app_settings.TIMEZONE))        
        from dateutil.relativedelta import relativedelta        
        three_mon_rel = relativedelta(months=12)
        target_date = str((today + three_mon_rel).date()) 
        win_prob = calc_win_prob(symbol, target_date, st.UNPAIRED, breakeven_l, np.nan)

        earning_date = get_next_earning_date(symbol)
        earning_date = "" if earning_date == None else str(earning_date)
        trade_stock_price = price  
        credit =  str(False)
        strategy = st.UNPAIRED                    

        cash = price * quantity
        margin = 0.0
    
        cash_position= self.get_BuyingPower() - cash        
        margin_position = self.get_margin_position()
        if math.isnan(margin_position):
            margin_position = 0.0

        last_price=open_price
        pl = 0.0
        gain = 0.0
        last_quote_date=trade_date
        last_stock_price = trade_stock_price
        status = asset.OPENED  
        fields = [ uuid, symbol, strategy, credit, open_price,\
                  trade_date,earning_date,trade_stock_price,quantity,status,\
                  cash, margin, cash_position, margin_position,\
                  last_price, pl, gain, last_quote_date, last_stock_price, target_low, target_high,\
                  breakeven_l, win_prob]

        field_names =  "uuid,symbol,strategy,credit,open_price,\
                        trade_date,earning_date,trade_stock_price,quantity,status,\
                        open_cash, open_margin, cash_position, margin_position,\
                        last_price, pl, gain, last_quote_date, last_stock_price,\
                        target_low, target_high, breakeven_l, win_prob"
        
        values = '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'

        if 'IB' in self.brokerage:
            live = False if 'PAPER' in self.brokerage else True
            srow = {}
            srow[pscl.SYMBOL] = symbol       
            srow[pscl.QUANTITY] = quantity
            srow[pscl.STRATEGY] = strategy
            srow[pscl.OPEN_PRICE] = open_price           
            x = place_ib_order(srow, TWS=ib_settings.TWS, live=live, bracket=False)
            if len(x.errorString) > 0:
                msg = "CREATE IB_ORDER FAILED %s [%s|%s] [pri:%.2f|prob:%.2f|q:%.2f] %s [%s]" %\
                    (x.ErrorCode, strategy, symbol, open_price, win_prob, quantity, self.account_name)
                self.logger.error(msg)
                status = asset.OPEN_FAILED
                field_names += ", ib_errorString, ib_errorCode, ib_advancedOrderRejectJson"
                fields += [x.ib_errorString, 
                          x.ib_errorCode, 
                          x.advancedOrderRejectJson]            
                values +=",?,?,?"                          
            else:            
                status = asset.OPEN_PENDING                    
                field_names += ", ib_clientId, ib_orderId, ib_status, ib_permId, ib_parentId, ib_clientId, ib_filled, ib_remaining, ib_avgFillPrice, ib_lastFillPrice, ib_whyHeld, ib_mktCapPrice, ib_tif"
                fields += [x.ib_clientId, 
                        x.ib_orderId, 
                        x.ib_status, 
                        x.ib_permId, 
                        x.ib_parentId, 
                        x.ib_clientId, 
                        x.ib_filled, 
                        x.ib_remaining, 
                        x.ib_avgFillPrice, 
                        x.ib_lastFillPrice, 
                        x.ib_whyHeld, 
                        x.ib_mktCapPrice, 
                        x.ib_tif]
                values +=",?,?,?,?,?,?,?,?,?,?,?,?,?"

        sql = "INSERT INTO position_summary ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)
        
        if 'IB' in self.brokerage:
            self.db_conn.commit()              
            if status == asset.OPEN_PENDING:
                msg = "OPEN PENDING [%s|%s] [pri:%.2f|prob:%.2f|q:%.2f][%s]" %\
                    (strategy, symbol, open_price, win_prob, quantity, self.account_name)
                
            if status == asset.FAIELD:
                msg = "OPEN FAILED %s %s [%s|%s] [pri:%.2f|prob:%.2f|q:%.2f][%s]" %\
                    (x.errorString, str(x.erroCode, strategy, symbol, open_price, win_prob, quantity, self.account_name))
                                
            return msg

        # Insert position record
        field_names =  "uuid, leg_id, symbol, otype, open_action,\
                        quantity,open_price,current_value,average_cost_basis,status,\
                        trade_date, init_volume"
        
        values =  '?,?,?,?,?,?,?,?,?,?,?,?' 

        fields = [uuid, leg_id, symbol, otype, open_action,\
                 quantity, open_price, current_value, average_cost_basis,status,\
                 trade_date, volume]    
        
        sql = "INSERT INTO position ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)

        trx_time = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")     
        amount = quantity * price       
        commission = 0
        fee = 0
        field_names =  "trx_time,symbol,otype,open_close,buy_sell,quantity,price,commission,fee,amount"
        values =  '?,?,?,?,?,?,?,?,?,?' 
        fields = [trx_time, symbol, otype, asset.OPEN, asset.BUY, quantity,\
                  price, commission, fee, amount]
        sql = "INSERT INTO transactions ("+field_names+") VALUES("+values+")" 
        cursor = self.db_conn.cursor()          
        cursor.execute(sql, fields)        
        self.__update_cash_position(cash_position, commit=False)  

        self.db_conn.commit()    
        msg = "BUY %s [price:%.2f|quantity:%d] %s" %\
             (symbol,open_price,quantity,self.account_name)
        self.logger.info(msg)   
        
        return msg

    def trade_ib_account(self, watchlist):
        from option_trader.entity.top_pick import top_pick_mgr, pick_catelog         
        pick_df = top_pick_mgr(self.user.site).get_top_pick_df(symbol_list=watchlist, pick_strategy=pick_catelog.MAX_LOSS_REALTIME)
        if pick_df.shape[0] == 0:
            self.logger.info('No candidate meet criteria')
            return []        
        #pick_df[pscl.QUANTITY] = pick_df.apply(lambda x: self.risk_mgr.max_loss_per_position//(100*x[pscl.MAX_LOSS]) if x[pscl.STRATEGY] != st.UNPAIRED else self.risk_mgr.max_loss_per_position/x[pscl.MAX_LOSS], axis = 1)  
        trade_rec_list = []
        row = pick_df.iloc[0]        
        #for i, row in pick_df.iterrows():     
        row[pscl.QUANTITY] = self.risk_mgr.max_loss_per_position//(100*row[pscl.MAX_LOSS]) if row[pscl.STRATEGY] != st.UNPAIRED else self.risk_mgr.max_loss_per_position/row[pscl.MAX_LOSS]      
        row[pscl.CREDIT] = str(True) if row[pscl.MARGIN] > 0 else str(False)              
        legs = row[pscl.LEGS]    
        for leg in legs:
            leg[pcl.QUANTITY] = leg[pcl.SCALE] * row[pscl.QUANTITY]
            leg[pcl.OPEN_PRICE] = leg['price'] 

        trade_rec = self.create_position_summary(row)  
        if len(trade_rec) > 0:
            trade_rec_list.append(trade_rec)

        self.logger.info('%s %s positions processed' % (self.account_name, len(trade_rec_list)))

        return trade_rec_list       
    
    def trade_position(self, watchlist=[], strategy_list=[]):
        
        acct_value = self.get_account_value()
        if acct_value == 0:
            return []

        cash = self.get_BuyingPower()
        cash_ratio = 100 * cash/acct_value 
        if cash_ratio < self.risk_mgr.min_cash_percent:
            self.logger.warning('Cash ratio %.2f lower than setting %2f' % (cash_ratio, self.risk_mgr.min_cash_percent))
            return []
                
        risk_matrix = self.get_risk_matrix()
        risk_ratio = risk_matrix[pscl.MAX_RISK]/acct_value 
        if risk_ratio  >=  (app_settings.RISK_MGR.max_risk_ratio/100):
            self.logger.warning('Risk ratio %.2f higher than setting %2f' % (risk_ratio, self.risk_mgr.max_risk_ratio))
            return []
        
        watchlist = watchlist if len(watchlist) > 0 else self.get_default_watchlist()

        strategy_list = strategy_list if len(strategy_list) > 0 else self.get_default_strategy_list()

        newlist = []                
        for symbol in watchlist:
            if symbol in risk_matrix[pscl.SYMBOL]:
               if risk_matrix[pscl.SYMBOL][symbol] < acct_value * self.risk_mgr.max_risk_per_asset /100:                
                    newlist.append(symbol)                
            else:
                newlist.append(symbol)                      
                
        if len(newlist) == 0:
            return []      
         
        watchlist = newlist

        if 'IB' in self.brokerage:        
            opened_df = self.get_position_summary(status=[asset.OPENED])    
            open_pending_df = self.get_position_summary(status=[asset.OPEN_PENDING])
            today = datetime.now(timezone(app_settings.TIMEZONE)).date()   
            open_pending_df['tdate'] = open_pending_df.apply(lambda x: pd.Timestamp(x[pscl.TRADE_DATE]).tz_convert(timezone(app_settings.TIMEZONE)).date(), axis = 1)
            open_pending_df = open_pending_df[open_pending_df['tdate']==today]
            all_def = pd.concat([opened_df, open_pending_df])        
            deleted_list = list(all_def[pscl.SYMBOL].unique())
            set_a = set(watchlist)
            set_b = set(deleted_list)
            watchlist = list(set_a - set_b)
            if len(watchlist) == 0:
                self.logger.warning("All in watchlist has one opened position!!")                
                return []
            
            trade_rec_list = self.trade_ib_account(watchlist)
        else:
            trade_rec_list = self.trade_account(watchlist, strategy_list, risk_matrix)

        return trade_rec_list

    
    def get_risk_matrix(self): 
        #brokerage = self.user.get_brokerage()          
        ops = self.get_position_summary(status=[asset.OPENED])
        if ops.shape[0] == 0:
            return {pscl.MAX_RISK: 0.0, 
                    pscl.SYMBOL:   {},
                    pscl.EXP_DATE: {},
                    pscl.STRATEGY: {} }
        
        ops[pscl.MAX_RISK] = ops.apply(lambda x: x[pscl.MAX_LOSS] * x[pscl.QUANTITY] * 100 if x[pscl.STRATEGY] != st.UNPAIRED else x[pscl.OPEN_PRICE], axis = 1)

        max_risk = ops[pscl.MAX_RISK].sum()

        symbol_risk = ops.groupby([pscl.SYMBOL]).sum(numeric_only=True)[pscl.MAX_RISK].to_dict()
        exp_date_risk = ops.groupby([pscl.EXP_DATE]).sum(numeric_only=True)[pscl.MAX_RISK].to_dict()
        strategy_risk = ops.groupby([pscl.STRATEGY]).sum(numeric_only=True)[pscl.MAX_RISK].to_dict()

        risk_matrix = {pscl.MAX_RISK:max_risk, 
                       pscl.SYMBOL:   symbol_risk,
                       pscl.EXP_DATE: exp_date_risk,
                       pscl.STRATEGY: strategy_risk }
        
        return risk_matrix
    
    def check_earning_date(self, watchlist):

        today = datetime.now(timezone(app_settings.TIMEZONE))        
        new_list = []
        for symbol in watchlist:

            df = self.user.site.get_monitor_df(filter=[symbol])
            if df.shape[0] == 1:
                earning = df.head(1)['earning'].values[0]
                if earning != "":
                    earning_date  = pd.Timestamp(earning).tz_localize(timezone(app_settings.TIMEZONE))                     
                else:
                    earning_date = None
            else:
                try:
                    earning_date = get_next_earning_date(symbol)
                except Exception as ex:
                    self.logger.exception(ex)
                    self.logger.info('%s earning date %s today %s' % (symbol, str(earning_date), str(today)))
                    continue        

            if earning_date is not None:
                days_to_earning = (earning_date - today).days               
                if days_to_earning <= self.risk_mgr.close_days_before_expire:
                    continue
                
            new_list.append(symbol)

        return new_list   

    def select_option_candidates(self, watchlist = [], strategy_list = []):

        watchlist = watchlist if len(watchlist) > 0 else self.get_default_watchlist()
 
        strategy_list = strategy_list if len(strategy_list) > 0 else self.get_default_strategy_list()   

        from option_trader.entity.top_pick import top_pick_mgr, pick_catelog     

        tp_df = top_pick_mgr(self.user.site).get_top_pick_df(watchlist, pick_strategy=pick_catelog.PREDICTED_RANGE)  
        if tp_df.shape[0] == 0:
            self.logger.error('Empty site top picks')
            return pd.DataFrame()    
                    
        candidates = tp_df[(tp_df[pscl.SYMBOL].isin(watchlist)) & (tp_df[pscl.STRATEGY].isin(strategy_list))]        

        if candidates.shape[0] > 0:

            candidates.sort_values([pscl.WIN_PROB, pscl.PNL],  ascending=False, inplace=True)                                                

            candidates[pscl.QUANTITY] = candidates.apply(lambda x: self.risk_mgr.max_loss_per_position//(100*x[pscl.MAX_LOSS]) if x[pscl.STRATEGY] != st.UNPAIRED else self.risk_mgr.max_loss_per_position/x[pscl.MAX_LOSS], axis = 1)  
        
            candidates = candidates[candidates[pscl.QUANTITY] > 0]

            candidates.drop_duplicates(subset=[pscl.SYMBOL, pscl.STRATEGY, pscl.EXP_DATE], inplace=True)

            df = self.get_position_summary(status=[asset.OPENED, asset.OPEN_PENDING])  

            candidates = candidates.merge(df.drop_duplicates(), on=[pscl.SYMBOL,pscl.STRATEGY, pscl.EXP_DATE], how='left', suffixes=('', '_to_be_deleted'), indicator=True)

            candidates[candidates['_merge'] == 'left_only']

            candidates[pscl.MAX_RISK] = candidates.apply(lambda x: x[pscl.MAX_LOSS] * x[pscl.QUANTITY] * 100 if x[pscl.STRATEGY] != st.UNPAIRED else x[pscl.OPEN_PRICE] * x[pscl.QUANTITY], axis = 1)  

            monitor_df = self.user.site.get_monitor_df(filter=watchlist)

            candidates = candidates.merge(monitor_df, on=[pscl.SYMBOL], how='left', suffixes=('', '_to_be_deleted'))

            candidates.drop(list(candidates.filter(regex='_to_be_deleted|_merge')), axis=1, inplace=True)

            trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date()

            candidates[pscl.TRADE_DATE] = trade_date

            candidates[pscl.LAST_QUOTE_DATE] = candidates['pick_date']

        return candidates

    def get_option_candidates(self, watchlist = [], strategy_list = []):

        watchlist = watchlist if len(watchlist) > 0 else self.get_default_watchlist()
 
        strategy_list = strategy_list if len(strategy_list) > 0 else self.get_default_strategy_list()   

        self.mdf  = self.get_position_summary(status=[asset.OPENED])

        candidates = pd.DataFrame()  # one per symbol     
        for strategy in strategy_list:
            if strategy   == st.LONG_CALL:
                df = self.pick_option_long( watchlist, asset.CALL)                
            elif strategy == st.LONG_PUT:
                df = self.pick_option_long( watchlist, asset.PUT)
            elif strategy == st.COVERED_CALL:
                df = self.pick_option_short( watchlist, asset.CALL)     
            elif strategy == st.SHORT_PUT:
                df = self.pick_option_short( watchlist, asset.PUT)                       
            elif strategy == st.CREDIT_CALL_SPREAD:
                df = self.pick_vertical_call_spread( watchlist, credit=True)            
            elif strategy == st.DEBIT_CALL_SPREAD:
                df = self.pick_vertical_call_spread( watchlist, credit=False)                                       
            elif strategy==  st.CREDIT_PUT_SPREAD:
                df = self.pick_vertical_put_spread( watchlist, credit=True)                     
            elif strategy == st.DEBIT_PUT_SPREAD:
                df = self.pick_vertical_put_spread( watchlist, credit=False)                    
            elif strategy==  st.CREDIT_IRON_CONDOR:
                df = self.pick_iron_condor( watchlist, credit=True)
            elif strategy == st.DEBIT_IRON_CONDOR:
                df = self.pick_iron_condor( watchlist, credit=False)                    
            elif strategy == st.CREDIT_PUT_BUTTERFLY:
                df = self.pick_put_butterfly( watchlist, credit=True)                                              
            elif strategy == st.CREDIT_CALL_BUTTERFLY:
                df = self.pick_call_butterfly( watchlist, credit=True)                                               
            elif strategy == st.DEBIT_PUT_BUTTERFLY:
                df = self.pick_put_butterfly( watchlist, credit=False)                 
            elif strategy == st.DEBIT_CALL_BUTTERFLY:
                df = self.pick_call_butterfly( watchlist, credit=False)      
            elif strategy == st.IRON_BUTTERFLY:
                df = self.pick_iron_butterfly( watchlist, credit=True)                          
            elif strategy == st.REVERSE_IRON_BUTTERFLY:
                df = self.pick_iron_butterfly( watchlist, credit=False)                                   
            elif strategy == st.WEEKLY_STOCK_TRADE:
                continue
            else:
                self.logger.error('Unsupported strategy %s' % strategy)
                continue                   

            self.logger.info('%s get %d candidates' %(strategy, df.shape[0]))

            candidates = pd.concat([candidates, df])        

        if candidates.shape[0] > 0:

            candidates.sort_values([pscl.WIN_PROB, pscl.PNL],  ascending=False, inplace=True)                                                

            candidates[pscl.QUANTITY] = candidates.apply(lambda x: self.risk_mgr.max_loss_per_position//(100*x[pscl.MAX_LOSS]) if x[pscl.STRATEGY] != st.UNPAIRED else self.risk_mgr.max_loss_per_position/x[pscl.MAX_LOSS], axis = 1)  
        
            candidates = candidates[candidates[pscl.QUANTITY] > 0]

            candidates.drop_duplicates(subset=[pscl.SYMBOL, pscl.STRATEGY, pscl.EXP_DATE], inplace=True)

            df = self.get_position_summary(status=[asset.OPENED])  

            candidates = candidates.merge(df.drop_duplicates(), on=[pscl.SYMBOL,pscl.STRATEGY, pscl.EXP_DATE], how='left', suffixes=('', '_to_be_deleted'), indicator=True)

            candidates[candidates['_merge'] == 'left_only']

            candidates[pscl.MAX_RISK] = candidates.apply(lambda x: x[pscl.MAX_LOSS] * x[pscl.QUANTITY] * 100 if x[pscl.STRATEGY] != st.UNPAIRED else x[pscl.OPEN_PRICE] * x[pscl.QUANTITY], axis = 1)  

            monitor_df = self.user.site.get_monitor_df(filter=watchlist)

            candidates = candidates.merge(monitor_df, on=[pscl.SYMBOL], how='left', suffixes=('', '_to_be_deleted'))

            candidates.drop(list(candidates.filter(regex='_to_be_deleted|_merge')), axis=1, inplace=True)

        return candidates

    def trade_account(self, watchlist, strategy_list, risk_matrix):   
        
        acct_value = self.get_account_value()
        if acct_value == 0:
            return []

        trade_rec_list = []
        if st.WEEKLY_STOCK_TRADE in strategy_list:
            trade_rec =  self.weekly_stock_play()
            if len(trade_rec) > 0:
                trade_rec_list.append(trade_rec)
            if len(strategy_list) == 1:
                return trade_rec_list

        candidates = self.select_option_candidates(watchlist=watchlist, strategy_list=strategy_list)
        if candidates.shape[0] == 0:
            return trade_rec_list
                 
        pos_selected = candidates.shape[0]

        exp_date_list = candidates[pscl.EXP_DATE].unique()
        exp_date_risk_list = risk_matrix[pscl.EXP_DATE]           
        for exp_date in exp_date_list:
            if exp_date in exp_date_risk_list:
                if  exp_date_risk_list[exp_date] > acct_value * self.risk_mgr.max_risk_per_expiration_date / 100:
                    candidates = candidates[candidates[pscl.EXP_DATE] != exp_date]

        symbol_list = candidates[pscl.SYMBOL].unique()
        symbol_risk_list = risk_matrix[pscl.SYMBOL]           
        for symbol in symbol_list:
            if symbol in symbol_risk_list:
                if  symbol_risk_list[symbol] > acct_value * self.risk_mgr.max_risk_per_asset / 100:
                    candidates = candidates[candidates[pscl.SYMBOL] != symbol]

        exp_date_list = sorted(exp_date_list)

        for exp_date in exp_date_list:
            targets = candidates[candidates[pscl.EXP_DATE] == exp_date]
            targets.sort_values([pscl.WIN_PROB, pscl.PNL],axis=0, ascending = False, inplace=True)

            #candidates = candidates.groupby([pscl.SYMBOL, pscl.EXP_DATE, pscl.STRATEGY]).first()
            for i, opt in targets.iterrows():  
                symbol =   opt[pscl.SYMBOL]
                exp_date = opt[pscl.EXP_DATE]
                strategy = opt[pscl.STRATEGY]             
                ps = self.get_position_summary(status=[asset.OPENED])         
                if ps[ (ps[pscl.SYMBOL]==symbol) & 
                    (ps[pscl.EXP_DATE]==exp_date) & 
                    (ps[pscl.STRATEGY]==strategy) ].shape[0] > 0:
                    continue

                symbol_risk = symbol_risk_list[symbol] if symbol in symbol_risk_list else 0.0
                if symbol_risk + opt[pscl.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_asset /100:
                    continue

                exp_risk = exp_date_risk_list[exp_date] if exp_date in exp_date_risk_list else 0.0
                if exp_risk + opt[pscl.MAX_RISK] > acct_value * self.risk_mgr.max_risk_per_expiration_date / 100:
                    continue
        
                if strategy == st.SHORT_PUT:
                    cash_avail = self.get_BuyingPower()
                    if (cash_avail - opt[pscl.MAX_RISK]) /acct_value  <  self.risk_mgr.min_cash_percent:
                        self.logger.info('No enough cash %.2f to sell put' % (cash_avail))
                        continue

                trade_rec = self.create_position_summary(opt)  
                if len(trade_rec) > 0:
                    trade_rec_list.append(trade_rec)
                    if exp_date not in exp_date_risk_list:
                        exp_date_risk_list[exp_date] = opt[pscl.MAX_RISK]
                    else:                         
                        exp_date_risk_list[exp_date] += opt[pscl.MAX_RISK]                 
                    if symbol not in symbol_risk_list:
                        symbol_risk_list[symbol] = opt[pscl.MAX_RISK]                      
                    else:
                        symbol_risk_list[symbol] += opt[pscl.MAX_RISK]
                    cash = self.get_BuyingPower()
                    cash_ratio = 100 * cash/acct_value 
                    if cash_ratio < self.risk_mgr.min_cash_percent:
                        self.logger.warning('Cash ratio %.2f lower than setting %2f' % (cash_ratio, self.risk_mgr.min_cash_percent))
                        self.logger.info('position %d selected %d created' % (pos_selected, len(trade_rec_list)))
                        return trade_rec_list
            
        self.logger.info('%s position %d selected %d created' % (self.account_name, pos_selected, len(trade_rec_list)))
        
        return trade_rec_list
    class optionLegDesc(object):
        def __init__(self, exp_date, leg):
            self.STRIKE       = leg[pcl.STRIKE]
            self.OTYPE        = leg[pcl.OTYPE] 
            self.OPEN_ACTION  = leg[pcl.OPEN_ACTION]
            self.QUANTITY     = leg[pcl.QUANTITY]
            self.PRICE        = leg[pcl.OPEN_PRICE]
            self.EXP_DATE     = exp_date
            self.IV           = leg[quote.IMPLIED_VOLATILITY]
            self.DELTA        = leg[quote.DELTA]            
            self.OPEN_INTEREST= leg[quote.OPEN_INTEREST]
  
    def create_transaction(self, pos, buy_sell, open_close, commission=0, fee=0):

        trx_time = datetime.now(timezone(app_settings.TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S %Z")     
        symbol = pos[pcl.SYMBOL]
        otype = pos[pcl.OTYPE]
        open_close = open_close
        buy_sell = buy_sell
        quantity =pos[pcl.QUANTITY]
        price = pos[pcl.LAST_PRICE]
        amount = quantity * price        
        commission = commission
        fee = fee
        amount = 0

        if otype in [asset.CALL, asset.PUT]:
            amount = quantity * price * 100                   
            strike = pos[pcl.STRIKE]
            exp_date = pos[pcl.EXP_DATE]

            field_names =  "trx_time,symbol,otype,strike,exp_date,open_close,buy_sell,quantity,price,commission,fee,amount"

            values =  '?,?,?,?,?,?,?,?,?,?,?,?' 

            fields = [trx_time, symbol, otype, strike, exp_date, open_close, buy_sell, quantity,\
                      price, commission, fee, amount]

            sql = "INSERT INTO transactions ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)
        elif otype == asset.STOCK:
            amount = quantity * price       

            field_names =  "trx_time,symbol,otype,open_close,buy_sell,quantity,price,commission,fee,amount"

            values =  '?,?,?,?,?,?,?,?,?,?' 

            fields = [trx_time, symbol, otype, open_close, buy_sell, quantity,\
                      price, commission, fee, amount]

            sql = "INSERT INTO transactions ("+field_names+") VALUES("+values+")" 
            cursor = self.db_conn.cursor()          
            cursor.execute(sql, fields)

    def get_account_summary(self):

        cl = summary_col_name

        summary = {}
        
        summary[cl.INIT_BALANCE] = round(self.get_initial_balance(),2)
        summary[cl.ACCT_VALUE] = round(self.get_account_value(),2)
        summary[cl.ASSET_VALUE] = round(self.get_asset_value(),2)
        summary[cl.CASH] = round(self.get_BuyingPower(),2)
        summary[cl.MARGIN] = round(self.get_margin_position(),2)   
        summary[cl.UNREALIZED_PL], summary[cl.REALIZED_PL] = self.get_pl()
        summary[cl.GAIN] = round(100 * ((summary[cl.UNREALIZED_PL]+summary[cl.REALIZED_PL]) / summary[cl.INIT_BALANCE]),2) if summary[cl.INIT_BALANCE] > 0 else 0

        #summary['open date'] = self.get_open_date()        

        o = self.get_position_summary()                
        tc = o.shape[0]        
        summary[cl.ALL_TRX_CNT] = tc
        summary[cl.AVG_ALL_TRX_WIN_PL] = round(o[o[pscl.GAIN]>0][pscl.PL].sum()/tc if tc > 0 else 0,2)
        summary[cl.AVG_ALL_TRX_LOSS_PL] = round(o[o[pscl.GAIN]<0][pscl.PL].sum()/tc if tc > 0 else 0,2)        
        summary[cl.ALL_WIN_RATE] = round(100*o[o[pscl.GAIN]>0].shape[0]/tc if tc > 0 else 0, 2)       

        oo = o[o[pscl.STATUS]==asset.OPENED]
        oo[cl.MAX_RISK] = oo.apply(lambda x: x[pscl.MAX_LOSS] * x[pscl.QUANTITY] * 100 if x[pscl.STRATEGY] != st.UNPAIRED else x[pscl.OPEN_PRICE], axis = 1)  
        summary[cl.MAX_RISK] = round(oo[cl.MAX_RISK].sum(),2)
        summary[cl.RISK_RATIO] = round(100*summary[cl.MAX_RISK]/summary[cl.ACCT_VALUE],2)

        oc = oo.shape[0]
        summary[cl.OPENED_TRX_CNT] = oc        
        summary[cl.AVG_OPENED_TRX_WIN_PL] = round(oo[oo[pscl.GAIN]>0][pscl.PL].sum()/oc if oc > 0 else 0,2)
        summary[cl.AVG_OPENED_TRX_LOSS_PL] = round(oo[oo[pscl.GAIN]<0][pscl.PL].sum()/oc if oc > 0 else 0,2)           
        summary[cl.OPENED_WIN_RATE] = round(100*oo[oo[pscl.GAIN]>0].shape[0]/oc if oc > 0 else 0,2)             

        co = o[(o[pscl.STATUS]== asset.CLOSED) | (o[pscl.STATUS]==asset.EXPIRED)]
        cc = co.shape[0]
        summary[cl.CLOSED_TRX_CNT] = cc                  
        summary[cl.AVG_CLOSED_TRX_WIN_PL] = round(co[co[pscl.GAIN]>0][pscl.PL].sum()/cc if cc > 0 else 0,2)
        summary[cl.AVG_CLOSED_TRX_LOSS_PL] = round(co[co[pscl.GAIN]<0][pscl.PL].sum()/cc if cc > 0 else 0,2)            
        summary[cl.CLOSED_WIN_RATE] = round(100*co[co[pscl.GAIN]>0].shape[0]/cc if cc > 0 else 0,2)      

        return summary
    #######################Helper##################################    

    def roll_option_long(self, symbol, exp_date_list, otype):
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_option_long( symbol, 
                                otype, 
                                predictlist,                
                                min_pnl = self.entry_crit.min_pnl,                                    
                                min_win_prob = self.entry_crit.min_chance_of_win,         
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)        
        return df  
        
    def roll_option_short(self, symbol, exp_date_list, otype):
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)              
        df = pick_option_short( symbol, 
                                otype, 
                                predictlist,            
                                min_pnl = self.entry_crit.min_pnl,                                         
                                min_win_prob = self.entry_crit.min_chance_of_win,
                                min_price = self.entry_crit.min_price_to_short,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)        
        return df
    
    def roll_vertical_call_spread(self, symbol, exp_date_list, credit=True):
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)
        df = pick_vertical_call_spreads(symbol,                          
                                        predictlist,
                                        credit=credit,
                                        max_spread = self.runtime_config.max_spread,                        
                                        min_win_prob=self.entry_crit.min_chance_of_win,
                                        min_pnl = self.entry_crit.min_pnl,
                                        max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                        max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                        min_open_interest=self.entry_crit.min_open_interest)                                               
        return df       

    def roll_vertical_put_spread(self, symbol, exp_date_list, credit=True):            
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)
        df = pick_vertical_put_spreads(symbol,                          
                                    predictlist,
                                    credit=credit,
                                    max_spread = self.runtime_config.max_spread,                        
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)   
            
        return df                

    def roll_iron_condor(self, symbol, exp_date_list,  credit=True):
        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_iron_condor(symbol,
                            predictlist,
                            credit=credit,                                           
                            max_spread = self.runtime_config.max_spread,
                            min_price = min_price,                              
                            min_win_prob=self.entry_crit.min_chance_of_win,
                            min_pnl = self.entry_crit.min_pnl,
                            max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                            max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                            min_open_interest=self.entry_crit.min_open_interest)
        return df                

    def roll_call_butterfly(self, symbol, exp_date_list, credit=True):

        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_call_butterfly(symbol,                          
                                predictlist,
                                credit=credit,       
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)            
        return df                
    
    def roll_put_butterfly(self, symbol, exp_date_list, credit=True):

        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_put_butterfly(symbol,                          
                                predictlist,
                                credit=credit,
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)
        return df    

    def roll_iron_butterfly(self, symbol, exp_date_list, credit=True):
        min_price = self.entry_crit.min_price_to_short if credit else 0.0   
        predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
        df = pick_iron_butterfly(symbol,                          
                                predictlist,
                                credit=credit,
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest) 
    
        return df                

    ############################       
      
    def pick_option_long(self, watchlist, otype):

        candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        pick_df = pd.DataFrame()

        if otype == asset.CALL:
            strategy_list = [st.LONG_CALL]
        else:
            strategy_list = [st.LONG_PUT]

        for symbol in candidates:

            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if otype == asset.CALL:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.LONG_CALL) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.LONG_PUT) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue

            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_option_long( symbol, 
                                    otype, 
                                    predictlist,                
                                    min_pnl = self.entry_crit.min_pnl,                                    
                                    min_win_prob = self.entry_crit.min_chance_of_win,         
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)        
        
            self.logger.info('pick_option_log %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])
    
        return pick_df    
    
    def pick_option_short(self, watchlist, otype):
        candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if otype == asset.CALL:    
                shares = self.get_stock_open_shares(symbol)
                q = shares // 100
                if q == 0:
                    self.logger.info('No enough %s shared %.2f to sell covered call' % (symbol, shares))
                    continue                 
                # TODO: check if covered call already consume all shares 
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.COVERED_CALL) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.SHORT_PUT) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)              
            df = pick_option_short( symbol, 
                                    otype, 
                                    predictlist,            
                                    min_pnl = self.entry_crit.min_pnl,                                         
                                    min_win_prob = self.entry_crit.min_chance_of_win,
                                    min_price = self.entry_crit.min_price_to_short,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)        

            self.logger.info('pick_option_short %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])
        return pick_df

    def pick_vertical_call_spread(self, watchlist, credit=True):
        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        pick_df = pd.DataFrame()

        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)

            if credit:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.CREDIT_CALL_SPREAD) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.DEBIT_CALL_SPREAD) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)
            min_price = self.entry_crit.min_price_to_short if credit else 0.0
            df = pick_vertical_call_spreads(symbol,                          
                                            predictlist,
                                            credit=credit,
                                            max_spread = self.runtime_config.max_spread,                        
                                            min_win_prob=self.entry_crit.min_chance_of_win,
                                            min_pnl = self.entry_crit.min_pnl,
                                            max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                            max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                            min_open_interest=self.entry_crit.min_open_interest)                           

            self.logger.info('pick_vertical_call_spread %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])
    
        return pick_df                

    def pick_vertical_put_spread(self, watchlist, credit=True):
        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        pick_df = pd.DataFrame()

        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        for symbol in candidates:    
            
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)

            if credit:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.CREDIT_PUT_SPREAD) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.DEBIT_PUT_SPREAD) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)

            #target = target_low if credit else target_high  

            df = pick_vertical_put_spreads(symbol,                          
                                        predictlist,
                                        credit=credit,
                                        max_spread = self.runtime_config.max_spread,                        
                                        min_win_prob=self.entry_crit.min_chance_of_win,
                                        min_pnl = self.entry_crit.min_pnl,
                                        max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                        max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                        min_open_interest=self.entry_crit.min_open_interest)   
            
            self.logger.info('pick_vertical_put_spread %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    

        return pick_df                

    def pick_iron_condor(self, watchlist, credit=True):

        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    
        
        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if credit:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.CREDIT_IRON_CONDOR) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.DEBIT_IRON_CONDOR) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue

            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_iron_condor(symbol,
                                predictlist,
                                credit=credit,                                           
                                max_spread = self.runtime_config.max_spread,
                                min_price = min_price,                              
                                min_win_prob=self.entry_crit.min_chance_of_win,
                                min_pnl = self.entry_crit.min_pnl,
                                max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_iron_condor %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
    
        return pick_df                

    def pick_call_butterfly(self, watchlist, credit=True):

        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if credit:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.CREDIT_CALL_BUTTERFLY) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.DEBIT_CALL_BUTTERFLY) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
                        
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_call_butterfly(symbol,                          
                                    predictlist,
                                    credit=credit,       
                                    max_spread = self.runtime_config.max_spread,
                                    min_price = min_price,                              
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_call_butterfly %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
        return pick_df                
    
    def pick_put_butterfly(self, watchlist, credit=True):

        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        min_price = self.entry_crit.min_price_to_short if credit else 0.0

        pick_df = pd.DataFrame()
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)

            if credit:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.CREDIT_PUT_BUTTERFLY) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.DEBIT_PUT_BUTTERFLY) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))

            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_put_butterfly(symbol,                          
                                    predictlist,
                                    credit=credit,
                                    max_spread = self.runtime_config.max_spread,
                                    min_price = min_price,                              
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_put_butterfly %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
        return pick_df    

    def pick_iron_butterfly(self, watchlist, credit=True):
        if credit:
            candidates = self.user.site.select_high_IV_HV_ratio_asset(self.entry_crit.min_IV_HV_ratio_for_short, filter=watchlist)    
        else:
            candidates = self.user.site.select_low_IV_HV_ratio_asset(self.entry_crit.max_IV_HV_ratio_for_long, filter=watchlist)    

        min_price = self.entry_crit.min_price_to_short if credit else 0.0
        pick_df = pd.DataFrame()        
        for symbol in candidates:
            exp_date_list = get_option_exp_date(symbol, min_days_to_expire=self.risk_mgr.open_min_days_to_expire, max_days_to_expire=self.runtime_config.max_days_to_expire)
            if credit:                
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.IRON_BUTTERFLY) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())
            else:
                data_list = set(self.mdf[(self.mdf[pscl.SYMBOL]==symbol) &
                                     (self.mdf[pscl.STRATEGY]==st.REVERSE_IRON_BUTTERFLY) &
                                     (self.mdf[pscl.STATUS]==asset.OPENED)][pscl.EXP_DATE].unique())

            exp_date_list = list(set(exp_date_list)-set(data_list))
            if len(exp_date_list) == 0:
                continue
            
            predictlist = predict_price_range(symbol, target_date_list=exp_date_list)      
            df = pick_iron_butterfly(symbol,                          
                                    predictlist,
                                    credit=credit,
                                    max_spread = self.runtime_config.max_spread,
                                    min_price = min_price,                              
                                    min_win_prob=self.entry_crit.min_chance_of_win,
                                    min_pnl = self.entry_crit.min_pnl,
                                    max_strike_ratio=self.runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=self.runtime_config.max_bid_ask_spread,
                                    min_open_interest=self.entry_crit.min_open_interest)

            self.logger.info('pick_butterfly %s get %d candidates' %(symbol, df.shape[0]))

            pick_df = pd.concat([pick_df, df])    
    
        return pick_df                

    def plot_account_history(acct, interactive=False):
        
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        plt.switch_backend('agg')

        df = acct.get_account_history()

        df.set_index("record date", inplace = True)

        plt.rcParams.update({'font.size': 15})        
        
        fig, axx= plt.subplots(figsize=(20,20), dpi=150) 
        fig.suptitle("Accunt History - user name:%s account name:%s]" %(acct.user.user_name, acct.account_name), fontsize=30)
        #ax1.remove()

        ax1 = plt.subplot2grid((40, 12), (0, 0), rowspan=9, colspan=14)   

        ax1.set_ylabel('Account values in $')
        #ax1.set_xlabel('Date', fontsize=8)

        ax1.plot(df['Acct Value'], color='orange') 
        ax1.plot(df['Initial Balance'], label='Initial Balance', linestyle='dotted')     
        ax1.plot(df['Cash'], color='green') 
        ax1.plot(df['Margin'], color='blue', alpha=0.35) 
        ax1.plot(df['Max Risk'], color='red', alpha=0.35) 
        
        ax1.legend(['Total Value', 'Inital Balance', 'Cash', 'Margin', 'Max Risk'], loc ="center left")
        ax1.grid()
        
        ax2 = plt.subplot2grid((40, 12), (10, 0), rowspan=6, colspan=14, sharex=ax1)  
        ax2.set_ylabel('PL')    
        ax2.plot(df['Realized PL'], color='blue') 
        ax2.plot(df['Unrealized PL'], color='green') 
        ax2.legend(['Realized PL', 'Unrealized PL'], loc ="center left")    
        ax2.grid()
        
        ax3 = plt.subplot2grid((40, 12), (17, 0), rowspan=6, colspan=14, sharex=ax1)  
        ax3.set_ylabel('Position Count')    
        ax3.plot(df['Trx # (all)'], color='blue') 
        ax3.plot(df['Trx# (opened)'], color='green') 
        ax3.plot(df['Trx# (closed)'], color='red') 
        ax3.legend(['All', 'Opened', 'Closed'], loc ="center left")    
        ax3.grid()
        
        ax4 = plt.subplot2grid((40,12), (24, 0), rowspan=6, colspan=14, sharex=ax1)
        ax4.set_ylabel('Win Rate & Risk Ratio')
        ax4.plot(df['Win Rate (all)']) 
        ax4.plot(df['Win Rate (opened)']) 
        ax4.plot(df['Win Rate (closed)']) 
        ax4.plot(df['Risk Ratio']) 
        ax4.legend(['All', 'Opened', 'Closed', 'Risk Ratio'], loc ="center left")
        ax4.grid()
        
        from option_trader.settings import ta_strategy  as  ta  

        output_path =  app_settings.CHART_ROOT_DIR + '/' + acct.user.user_name+acct.account_name +'_user_account_history.png'

        plt.savefig(output_path, bbox_inches='tight')       

        if interactive:
            plt.show()    

        plt.close() 

        return output_path

if __name__ == '__main__':

    import sys

    sys.path.append(r'\\Users\\jimhu\\option_trader\src')
    
    from option_trader.admin.site import site
    from option_trader.admin import user
    from option_trader.consts import strategy as st

    logging.basicConfig(level=logging.WARNING)

    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
    logging.getLogger('yfinance').setLevel(logging.WARNING)
    
    DEFAULT_SITE_STRATEGY = [st.CREDIT_PUT_SPREAD, st.CREDIT_IRON_CONDOR]
    
    watchlist = ['MSFT', 'AAPL', 'AMZN', 'NVDA', 'BLDR', 'COST', 'GOOGL', 'NFLX', 'META', 'SPY', 'QQQ', 'AMD', 'TSLA', 'ISRG']

    mysite = site('mysite', check_afterhour=False)

    from option_trader.utils.data_getter_ib import accounts_values_profolio, accounts_openOrders 
    from option_trader.utils.data_getter_ib import IBClient

    from threading import Timer

    ib_user_paper = mysite.get_user('ib_user_paper')
    
    ib_user_live = mysite.get_user('ib_user_live')

    #ib_user_paper.syncup_brokerage_accounts()


    #ib_user_live.syncup_brokerage_accounts()

    DU8147717_acct = ib_user_paper.get_account('DU8147717')

    DU8147717_acct.update_position()
    
    exit(0)

    #print(DU8147717_acct.load_ib_porforlio())

    #U11921459_acct = ib_user_live.get_account('U11921459')

    #print('U11921459 asset value',U11921459_acct.get_asset_value())    
    #print('U11921459 cash position', U11921459_acct.get_BuyingPower())
    #print('U11921459 margin position',U11921459_acct.get_margin_position())
    #print('U11921459 pl',U11921459_acct.get_pl())


    print('DU8147717 asset value',DU8147717_acct.get_asset_value())    
    print('DU8147717 cash position', DU8147717_acct.get_BuyingPower())
    print('DU8147717 margin position',DU8147717_acct.get_margin_position())
    print('DU8147717 pl',DU8147717_acct.get_pl())

    #ib_user_paper.syncup_brokerage_accounts()

    #df = DU8147717_acct.get_ib_account_portfolio()

    #DU8147717_acct.open_new_strategy_positions()

    DU814771_acct.open_new_strategy_positions()
    #DU8147717_acct.update_position()

    exit(0)

    values_dict, profolio_df = refresh_ib_accounts_values_protfolio(TWS=True, Live=True)
    for account_name in values_dict.keys():
        acct = ib_user.get_account(account_name)
        acct.save_ib_account_values(values_dict[account_name])
        acct.save_ib_account_portfolio(profolio_df[profolio_df['accountName']==account_name])

    exit(0)


    DU814771_acct = ib_user.get_account('DU814771')
    DU814771_acct.open_new_strategy_positions()


    with IBClient(TWS=True, Live=False) as ibClient:
        accountList = ib_user.get_account_list()
        order_df = ibClient.get_accounts_openOrders()
        for account_name in accountList:
            o_df = order_df[order_df['account']==account_name] 
            if o_df.shape[0] == 0:
                continue                       
            acct = ib_user.get_account(account_name)
            acct.save_ib_account_openOrders(o_df)

    exit(0)

    with IBClient(TWS=True, Live=False) as ibClient:
        accountList = ib_user.get_account_list()
        details_df = ibClient.get_execution_details()
        for account_name in accountList:                   
            acct = ib_user.get_account(account_name)
            acct.save_ib_execution_details(details_df)

    exit(0)


    mysite = site('mysite')
    u = mysite.get_user('ib_user')
    account_list = u.get_account_list()
    for account_name in account_list:
        a = u.get_account(account_name)
        a.update_position()
        a.open_new_strategy_positions()

    exit()

    exit(0)

    mysite = site('mysite')
    real_user = mysite.get_user('stester')
    real_bullish= real_user.get_account('spread')
    real_bullish.open_new_strategy_positions()

    exit(0)


    with site('mysite') as mysite:        
        trade_rec_list = []
        user_list = mysite.get_user_list()
        for user_name in user_list:
            if user_name == 'ib_user':
                continue
            this_user = mysite.get_user(user_name)
            account_list = this_user.get_account_list()
            for account_name in account_list:
                this_account = this_user.get_account(account_name)
                #this_account.open_new_strategy_positions()                
                trade_rec_list += this_account.update_position()
                   
    exit()

    real_user = mysite.get_user('real')
    real_bullish= real_user.get_account('bullish')
    #real_bearish= real_user.get_account('bearish')    
    #real_neutral= real_user.get_account('neutral')
    #real_bigmove= real_user.get_account('bigmove')

    real_bullish.open_new_strategy_positions()
    #real_bearish.open_new_strategy_positions()
    #real_neutral.open_new_strategy_positions()
    #real_bigmove.open_new_strategy_positions()

    #x = algo_11_07_iron_condor.open_new_strategy_positions(watchlist=watchlist, strategy_list=st.ALL_STRATEGY)  

    #print(len(x))

    exit(0)


    ib_user = mysite.get_user('ib_user')

    app = accounts_openOrders(ib_user)
    app.connect("127.0.0.1", 7497, 0)                
    t = Timer(200, app.stop)
    t. start()
    app.run()
    t.cancel()

    for account_name in app.accountList:
        acct = ib_user.get_account(account_name)
        if app.open_orders.shape[0] == 0:
           acct.save_ib_account_openOrders(pd.DataFrame())
        else:
            acct.save_ib_account_openOrders(app.open_orders[app.open_orders['account']==account_name])

    exit(0)

    app = accounts_values_profolio(ib_user)
    app.connect("127.0.0.1", 4001, 0)                
    t = Timer(200, app.stop)
    t. start()
    app.run()
    t.cancel()

    for account_name in app.accountList:
        acct = ib_user.get_account(account_name)
        acct.save_ib_account_values(app.accountValue_dict[account_name])
        acct.save_ib_account_portfolio(app.accountPortfolio_df[app.accountPortfolio_df['accountName']==account_name])
    exit(0)


    app = get_accounts_positions(ib_user)
    app.connect("127.0.0.1", 4001, 0)                
    t = Timer(200, app.stop)
    t. start()
    app.run()
    t.cancel()

    for account_name in app.accountList:
        acct = ib_user.get_account(account_name)
        acct.save_ib_account_positions(app.pos[app.pos['account']==account_name])

    exit(0)

    app = get_accounts_summary(ib_user)
    app.connect("127.0.0.1", 4001, 0)                
    t = Timer(200, app.stop)
    t. start()
    app.run()
    t.cancel()

    for account_name in app.accountList:
        acct = ib_user.get_account(account_name)
        acct.save_ib_daily_account_summary(app.accountSummary_df.loc[account_name])

    exit(0)
    app = get_accounts_summary(ib_user)
    app.connect("127.0.0.1", 4001, 0)                
    t = Timer(200, app.stop)
    t. start()
    app.run()
    t.cancel()

    for account_name in app.accountList:
        acct = ib_user.get_account(account_name)
        acct.save_ib_daily_account_summary(app.accountSummary_df.loc[account_name])

    exit(0)

    for account_name in account_list:
        print('%s update Account %s' % (stester.user_name, account_name))
        #account_obj = stester.get_account(account_name)
        #account_obj.update_position()
        account_obj.open_new_strategy_positions()

    exit(0)
    real_user = mysite.get_user('real')
    real_bullish= real_user.get_account('bullish')
    real_bearish= real_user.get_account('bearish')    
    real_neutral= real_user.get_account('neutral')
    real_bigmove= real_user.get_account('bigmove')

    #real_bullish.open_new_strategy_positions()
    real_bearish.open_new_strategy_positions()
    real_neutral.open_new_strategy_positions()
    real_bigmove.open_new_strategy_positions()

    #x = algo_11_07_iron_condor.open_new_strategy_positions(watchlist=watchlist, strategy_list=st.ALL_STRATEGY)  

    #print(len(x))

    exit(0)




    winwin_act = winwin.create_account('butterfly')

    winwin_act.get_position_summary()

    exit(0)

  

    jihuang = mysite.create_user('jihuang')

    account_list = jihuang.get_account_list()

    for account_name in account_list:
        print('%s update Account %s' % (jihuang.user_name, account_name))
        account_obj = jihuang.get_account(account_name)
        account_obj.update_position()
  