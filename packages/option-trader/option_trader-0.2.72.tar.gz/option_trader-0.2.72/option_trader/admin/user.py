
import pandas as pd
import os
import json   

from option_trader.settings import app_settings  as settings    
from option_trader.settings import schema as schema  

from option_trader.utils.line_norify import lineNotifyMessage 
from option_trader.admin.account import account, summary_col_name as cl
from option_trader.settings import app_settings
from option_trader.entity.position_summary import position_summary_col_name as pscl

from datetime import time, date, datetime, timedelta
from pytz import timezone

import re
import sqlite3

from json2html import *   

import logging

class user():  

    def __init__(self, 
                 site, 
                 user_name,
                 email="askme@outlook.com",
                 watchlist=[],
                 strategy_list=[]                   
                 ):
        
        self.site = site
        self.user_name = user_name

        self.logger = logging.getLogger(__name__)
        self.user_home_dir = os.path.join(site.user_root, self.user_name)        
        self.report_dir = os.path.join(self.user_home_dir, 'reports') 

        if os.path.exists(self.user_home_dir) == False:
            os.mkdir(self.user_home_dir)

        if os.path.exists(self.report_dir) == False:
            os.mkdir(self.report_dir)

        if settings.DATABASES == 'sqlite3':      

            self.db_path = os.path.join(self.user_home_dir,self.user_name+"_user.db")                     

            try:   
                if os.path.exists(self.db_path): 
                    self.db_conn  = sqlite3.connect(self.db_path)                   
                    self.email = self.get_user_email()
                    self.default_strategy_list = self.get_default_strategy_list()
                    self.default_watchlist = self.get_default_watchlist()
                    self.notification_token = self.get_notification_token()
                    #cursor = self.db_conn.cursor()
                    #cursor.execute('''ALTER TABLE user_profile ADD COLUMN brokerage TEXT''')
                    self.db_conn.commit()                                      
                    self.brokerage = self.get_brokerage()                    
                else:                                         
                    if os.path.exists(self.user_home_dir) == False:        
                        os.mkdir(self.user_home_dir)                    
                    self.default_strategy_list = site.default_strategy_list if len(strategy_list) == 0 else strategy_list
                    self.default_watchlist = site.default_watchlist if len(watchlist) == 0 else watchlist
                    self.notification_token     = site.get_default_notification_token()                
                    self.db_conn  = sqlite3.connect(self.db_path)  
                    cursor = self.db_conn.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS user_profile("+schema.user_profile+")")
                    cursor.execute("CREATE TABLE IF NOT EXISTS account_list("+schema.account_list+")")
                    #cursor.execute("CREATE TABLE IF NOT EXISTS watchlist("+schema.watchlist+")")                                             
                    sql = "INSERT INTO user_profile (name, email, default_strategy_list, default_watchlist, notification_token) VALUES (?, ?, ?, ?, ?)"                              
                    self.email = email
                    cursor.execute(sql, [user_name, self.email, json.dumps(self.default_strategy_list), json.dumps(self.default_watchlist), self.notification_token])
                    self.db_conn.commit()                 
            except Exception as e:
                self.logger.error(e)       
                raise e
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)

        #self.syncup_brokerage_accounts()

    def __enter__(self):
        return self
 
    def __exit__(self, *args):
        try:
            self.db_conn.close()
        except Exception as ex:
            self.logger.exception(ex)
            raise ex
                    
    # create new account        
    def delete_get_user_profile(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT email, default_strategy FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                profile = cursor.fetchone()
                return profile[0], json.loads(profile[1]) 
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")
        return None, None
    
    def get_default_strategy_list(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_strategy_list FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")
           
    def get_default_watchlist(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT default_watchlist FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return json.loads(cursor.fetchone()[0])                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_notification_token(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT notification_token FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]                   
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_user_email(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT email FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                return cursor.fetchone()[0]
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def get_brokerage(self):
        if settings.DATABASES == 'sqlite3':                 
            try:    
                sql = "SELECT brokerage FROM user_profile"                
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                b = cursor.fetchone()[0] 
                return "" if b == None else b
            except Exception as e:
                self.logger.exception(e)
                return ""
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_default_strategy_list(self, strategy_list):
        if len(strategy_list) == 0:
            self.logger.error('Cannot set empty default strategy list')
            return [] 
              
        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET default_strategy_list='"+json.dumps(strategy_list)+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()                 
                self.default_strategy_list = strategy_list
            except Exception as e:
                self.logger.exception(e)
                return []
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_default_watchlist(self, watchlist):
            
        if len(watchlist) == 0:
            self.logger.error('Cannot set empty default watchlist!')
            return []
        
        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET default_watchlist='"+json.dumps(watchlist)+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()
                self.default_watchlist = watchlist         
                self.site.expand_monitor_list(watchlist)
                return watchlist        
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_notification_token(self, token):
            
        if len(token) != len(app_settings.LINE_NOTIFICATION_TOKEN):
            self.logger.error('Invalid notification token %s' %token)

        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET notification_token='"+token+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()         
                self.notification_token = token
                return token        
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")
            return ''

    def update_user_email(self, email):

        if len(email) == 0:
            return    
            
        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET email='"+email+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()                 
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def update_brokerage(self, brokerage): 
            
        if settings.DATABASES == 'sqlite3':                 
            try:                              
                sql = "UPDATE user_profile SET brokerage='"+brokerage+"' WHERE name='"+self.user_name+"'"                    
                cursor = self.db_conn.cursor()                    
                cursor.execute(sql)
                self.db_conn.commit()                 
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error("sqlite3 only for now %s")

    def create_account(self, 
                       account_name,
                        initial_balance=app_settings.DEFAULT_ACCOUNT_INITIAL_BALANCE,                       
                        watchlist=[], 
                        strategy_list=[]):       
        
        if settings.DATABASES == 'sqlite3':                
            try:
                account_list = self.get_account_list()
                if account_name in account_list:
                    account_db_path = os.path.join(self.user_home_dir,account_name+"_account.db")    

                    if os.path.exists(account_db_path) :                                       
                        self.logger.warning('Account %s already exist return existing one' % account_name)
                        return account(self, account_name)
                    else:
                        self.logger.warning('Account %s DB recreated' % account_name)                        
                        return account(self, account_name, initial_balance=initial_balance, watchlist=watchlist, strategy_list=strategy_list)
                            
                a = account(self, 
                            account_name, 
                            initial_balance=initial_balance,
                            watchlist=watchlist,
                            strategy_list=strategy_list)
                             
                sql = "INSERT INTO account_list VALUES (?,?)"       
                cursor = self.db_conn.cursor()
                cursor.execute(sql, [account_name, a.db_path]) 
                self.db_conn.commit()            
                return a
            except Exception as e:
                self.logger.exception(e)
                raise e     

    def get_account_list(self):
        if settings.DATABASES == 'sqlite3':                
            try:
                cursor = self.db_conn.cursor()                    
                account_name_list = [account_name[0] for account_name in cursor.execute("SELECT account_name FROM account_list")]
                return account_name_list
            except Exception as e:
                self.logger.exception(e)
                raise e
        else:
            self.logger.error('Unsupported database engine %s' % settings.DATABASES)

    def get_account(self, account_name):
        account_name_list = self.get_account_list()
        if account_name in account_name_list:
            return account(self, account_name)
        else:
            raise ValueError('%s not found' % (account_name))
    
    def send_trade_report(self, account_name_list, trade_rec_list):

        if len(trade_rec_list) == 0:
            return

        to_addr = self.get_user_email()
        
        from time import ctime

        from option_trader.utils.gmail_notify import send_mail 

        import socket

        hostname = socket.gethostname()  

        send_mail(app_settings.MY_GMAIL_USER,  
                    [to_addr], 
                    'Trade Report!! ('+ ctime() + ') from ['+hostname+']', 
                    "Trade Report for " + self.user_name  + '|' + '.'.join(account_name_list) ,
                    json2html.convert(json = json.dumps(trade_rec_list)),             
                    [])

    def send_account_status_report(self):

        to_addr = self.get_user_email()
        
        from time import ctime

        from option_trader.utils.gmail_notify import send_mail 
        import option_trader.consts.strategy as st
        from option_trader.consts import asset   

        from  option_trader.entity import position_summary
        import socket

        hostname = socket.gethostname()  

        account_list = self.get_account_list()

        if len(account_list)== 0:
            return
        
        account_df = pd.DataFrame()

        position_df = pd.DataFrame()

        mail_body = ""

        files = []

        for account_name in account_list:
            acct = self.get_account(account_name)
            hist_path = acct.plot_account_history()         
            if os.path.exists(hist_path):
                files.append(hist_path)
            else:
                self.logger.error('account history file %s not found' % hist_path)            
            init_balance = acct.get_initial_balance()
            open_date = acct.get_open_date()
            d = acct.create_daily_account_summary()       
            #d = acct.get_account_history().tail(1)
            e = acct.get_position_summary(status=[asset.OPENED])
            e.insert(0, 'account name', account_name)
            d.insert(0, 'account name', account_name)                 
            #d.at[d.index[0], 'Gain %'] =  round(100 * (d.at[d.index[0], 'account value'] - init_balance)/ init_balance, 2)       
            #d.at[d.index[0], 'Initial Balance'] =  round(init_balance, 2)      
            #d.at[d.index[0], 'Created Date'] = open_date                

            account_df = pd.concat([account_df, d])
            position_df = pd.concat([position_df, e])

        account_summary = account_df[['account name', 
                                      cl.ACCT_VALUE, 
                                      cl.ASSET_VALUE, 
                                      cl.CASH, 
                                      cl.MARGIN, 
                                      cl.REALIZED_PL, 
                                      cl.UNREALIZED_PL, 
                                      cl.MAX_RISK,
                                      cl.RISK_RATIO,
                                      cl.INIT_BALANCE,
                                      cl.GAIN]]

        import numpy as np

        mail_body = "<h3>Account Summary</h3>" + account_summary.to_html(index=False)

        account_statistics = account_df[['account name', 
                                      cl.ALL_TRX_CNT,
                                      cl.OPENED_TRX_CNT,
                                      cl.CLOSED_TRX_CNT,

                                      cl.ALL_WIN_RATE,
                                      cl.OPENED_WIN_RATE,
                                      cl.CLOSED_WIN_RATE,

                                      cl.AVG_ALL_TRX_WIN_PL,
                                      cl.AVG_OPENED_TRX_WIN_PL,
                                      cl.AVG_CLOSED_TRX_WIN_PL,

                                      cl.AVG_ALL_TRX_LOSS_PL,
                                      cl.AVG_OPENED_TRX_LOSS_PL,
                                      cl.AVG_CLOSED_TRX_LOSS_PL]]                                      

        account_statistics.columns  = [sub.replace('Trx', 'Contract') for sub in account_statistics.columns] 
        mail_body += "<h3>Account Statistics</h3>" + account_statistics.to_html(index=False)

        from option_trader.entity.monitor import cname

        monitor_df = self.site.get_monitor_df()[[cname.symbol, cname.last_quote, cname.ten_days_gain, cname.ten_days_low, cname.ten_days_high, cname.exp_1_IV_HV_dif, cname.earning]]

        monitor_df['dist. to 10d high'] = monitor_df.apply(lambda x: (x[cname.ten_days_high]-x[cname.last_quote]) / (x[cname.ten_days_high]-x[cname.ten_days_low]), axis = 1) 

        today = datetime.now(timezone(app_settings.TIMEZONE))

        #monitor_df['days to earning'] = monitor_df.apply(lambda x: np.nan if x['earning'] == "" else (pd.Timestamp(x['earning']).tz_localize(timezone(app_settings.TIMEZONE))-today).days, axis = 1)

        position_df = position_df.merge(monitor_df.drop_duplicates(), on=[pscl.SYMBOL], how='left', suffixes=('', '_from_monitor'), indicator=True)

        position_df['days to earning'] = position_df.apply(lambda x: np.nan if x[cname.earning] == "" else (pd.Timestamp(x['earning']).tz_localize(timezone(app_settings.TIMEZONE))-today).days, axis = 1)

        stock_position = position_df[position_df[pscl.STRATEGY] == st.UNPAIRED]

        option_position = position_df[position_df[pscl.STRATEGY] != st.UNPAIRED] 
        option_position[pscl.GAIN] = option_position.apply(lambda x: round(x[pscl.GAIN],3) if np.isnan(x[pscl.GAIN]) != True else np.nan, axis = 1)  
        option_position[pscl.MAX_RISK] = option_position.apply(lambda x: round(x[pscl.MAX_LOSS] *  x[pscl.QUANTITY] * 100,2), axis = 1) 
        option_position[pscl.MAX_PROFIT] = option_position.apply(lambda x: round(x[pscl.MAX_PROFIT] *  x[pscl.QUANTITY] * 100,2), axis = 1) 
        stock_position[pscl.MAX_RISK] = stock_position.apply(lambda x: round(x[pscl.OPEN_PRICE] *  x[pscl.QUANTITY],2), axis = 1) 

        if position_df.shape[0] > 0:         
            total_option_risk = option_position[pscl.MAX_RISK].sum() if option_position.shape[0] > 0 else 0
            total_stock_risk  = stock_position[pscl.MAX_RISK].sum() if stock_position.shape[0] > 0 else 0
            symbol_summary = pd.DataFrame()            
            i = 0
            slist = position_df[pscl.SYMBOL].unique()
            for symbol in slist:
                op = option_position[option_position[pscl.SYMBOL] == symbol]              
                sp = stock_position[stock_position[pscl.SYMBOL] == symbol]              
           
                symbol_summary.at[i, pscl.SYMBOL] = symbol
                symbol_summary.at[i, 'Contract #'] = op.shape[0]
                symbol_summary.at[i, 'Share #'] = sp[pscl.QUANTITY].sum() if sp.shape[0] > 0 else ""
                option_pl = op[pscl.PL].sum() if op.shape[0] > 0 else 0
                symbol_summary.at[i, 'PL (option)'] = round(option_pl,2)                
                stock_pl = sp[pscl.PL].sum() if sp.shape[0] > 0 else 0
                symbol_summary.at[i, 'PL (stock)'] = round(stock_pl,2)                
                max_option_risk = op[pscl.MAX_RISK].sum() if op.shape[0] > 0 else 0
                max_stock_risk  = sp[pscl.MAX_RISK].sum() if sp.shape[0] > 0 else 0
                symbol_summary.at[i, 'Max Risk (option)'] = max_option_risk
                symbol_summary.at[i, 'Risk Ratio% (option)'] = round(100*max_option_risk/total_option_risk,2) if total_option_risk > 0 else 0                                             
                symbol_summary.at[i, 'Max Risk (stock)'] = max_stock_risk
                symbol_summary.at[i, 'Risk Ratio% (stock)'] = round(100*max_stock_risk/total_stock_risk,2) if total_stock_risk > 0 else 0                                            
                win_count = op[op[pscl.PL]>0].shape[0] if op.shape[0] > 0 else 0
                symbol_summary.at[i, 'Win Rate% (option)'] = round(100*win_count/op.shape[0],2) if op.shape[0] > 0 else 0  
                i += 1    
            
            symbol_summary.sort_values(pscl.SYMBOL, inplace=True )
            mail_body += "<h3>Symbol Statistics</h3>" + symbol_summary.to_html(index=False)   

            if option_position.shape[0] > 0:
                exp_date_list = option_position[pscl.EXP_DATE].unique()      
                exp_date_summary = pd.DataFrame()            
                i = 0                          
                for exp_date in exp_date_list:
                    ep = option_position[option_position[pscl.EXP_DATE]==exp_date]
                    if ep.shape[0] == 0:
                        continue
                    exp_date_summary.at[i, 'Exp Date'] = exp_date
                    exp_date_summary.at[i, 'Contract #'] = ep.shape[0]
                    max_risk = ep[pscl.MAX_RISK].sum()
                    exp_date_summary.at[i, 'Max Risk'] = max_risk
                    exp_date_summary.at[i, 'PL'] = ep[pscl.PL].sum()
                    exp_date_summary.at[i, 'Risk Ratio%'] = round(100*max_risk/total_option_risk,2)                                              
                    win_count = ep[ep[pscl.PL]>0].shape[0]
                    exp_date_summary.at[i, 'Win Rate%'] = round(100*win_count/ep.shape[0],2)                       
                    i += 1
                exp_date_summary.sort_values('Exp Date', inplace=True)
                mail_body += "<h3>Exp. Date Statistics</h3>" + exp_date_summary.to_html(index=False)   

                strategy_list = option_position[pscl.STRATEGY].unique()      
                strategy_summary = pd.DataFrame()            
                i = 0                          
                for strategy in strategy_list:
                    sp = option_position[option_position[pscl.STRATEGY]==strategy]
                    if sp.shape[0] == 0:
                        continue
          
                    strategy_summary.at[i, 'Strategy'] = strategy
                    strategy_summary.at[i, 'Contract #'] = sp.shape[0]
                    max_risk = sp[pscl.MAX_RISK].sum()
                    strategy_summary.at[i, 'Max Risk'] = max_risk
                    strategy_summary.at[i, 'PL'] = sp[pscl.PL].sum()
                    strategy_summary.at[i, 'Risk Ratio%'] = round(100*max_risk/total_option_risk,2) 
                    win_count = sp[sp[pscl.PL]>0].shape[0]
                    strategy_summary.at[i, 'Win Rate%'] = round(100*win_count/sp.shape[0],2)                                                
                    i += 1
                strategy_summary.sort_values('Strategy', inplace=True)
                mail_body += "<h3>Strategy Statistics</h3>" + strategy_summary.to_html(index=False)   

        if stock_position.shape[0] > 0:            
            mail_body += '<h3>Stock Positions</h3>'            
            account_list = stock_position['account name'].unique()                    
            for account_name in account_list:
                account_stock_position = stock_position[stock_position['account name']==account_name] #[[pscl.SYMBOL, pscl.QUANTITY, pscl.TRADE_DATE, pscl.OPEN_PRICE, pscl.LAST_STOCK_PRICE, pscl.GAIN]]
                #act = account_stock_position.merge(monitor_df, how='left')                
                account_stock_position.sort_values(pscl.TRADE_DATE, inplace=True)
                
                account_stock_position[pscl.OPEN_PRICE] = round(account_stock_position[pscl.OPEN_PRICE],2)

                stock_summary = account_stock_position[[pscl.SYMBOL, 
                                                        pscl.QUANTITY, 
                                                        pscl.TRADE_DATE, 
                                                        pscl.OPEN_PRICE, 
                                                        pscl.LAST_STOCK_PRICE,  
                                                        pscl.GAIN, 
                                                        pscl.PL,                                                         
                                                        'dist. to 10d high', 
                                                        cname.ten_days_gain, 
                                                        cname.ten_days_low, 
                                                        cname.ten_days_high, 
                                                        cname.exp_1_IV_HV_dif,
                                                        cname.earning,
                                                        'days to earning']]
                stock_summary[pscl.OPEN_PRICE] = stock_summary.apply(lambda x: round(x[pscl.OPEN_PRICE],3) if np.isnan(x[pscl.OPEN_PRICE]) != True else np.nan, axis = 1)  
                stock_summary[pscl.LAST_STOCK_PRICE] = stock_summary.apply(lambda x: round(x[pscl.LAST_STOCK_PRICE],3) if np.isnan(x[pscl.LAST_STOCK_PRICE]) != True else np.nan, axis = 1)  
                stock_summary[pscl.GAIN] = stock_summary.apply(lambda x: round(x[pscl.GAIN],3) if np.isnan(x[pscl.GAIN]) != True else np.nan, axis = 1)  
                stock_summary[pscl.PL] = stock_summary.apply(lambda x: round(x[pscl.PL],3) if np.isnan(x[pscl.PL]) != True else np.nan, axis = 1)  
                stock_summary['dist. to 10d high'] = stock_summary.apply(lambda x: round(x['dist. to 10d high'],3) if np.isnan(x['dist. to 10d high']) != True else np.nan, axis = 1)  

                stock_summary.sort_values(pscl.SYMBOL, inplace=True)
                stock_summary.columns  = [sub.replace('_', ' ') for sub in stock_summary.columns]
                mail_body += '<h4>'+account_name+'</h4>'+stock_summary.to_html(index=False) 

        if option_position.shape[0] > 0:         
               
            mail_body += '<h3>Opened Option Contracts</h3>'   

            exp_date_list = option_position[pscl.EXP_DATE].unique()
            exp_date_list.sort()
            for exp_date in exp_date_list:
                days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days
                #option_summary = option_position[option_position[pscl.EXP_DATE]==exp_date]
                exp_date_option_position = option_position[option_position[pscl.EXP_DATE]==exp_date]
                if exp_date_option_position.shape[0] == 0:
                    continue
                
                mail_body += '<h4>Exp. Date: %s DTE %d</h4>' % (str(exp_date), days_to_expire)

                account_list = exp_date_option_position['account name'].unique()                    
                for account_name in account_list:
                    symbol_option_position = exp_date_option_position[exp_date_option_position['account name']==account_name]
                    if symbol_option_position.shape[0] == 0:
                        continue
                    max_risk = symbol_option_position[pscl.MAX_RISK].sum()
                    symbol_option_position.sort_values(pscl.GAIN, inplace=True)
                    display = symbol_option_position[[pscl.SYMBOL, pscl.STRATEGY, pscl.QUANTITY, pscl.MAX_PROFIT, pscl.MAX_RISK, pscl.PL, pscl.GAIN, 'days to earning', pscl.LAST_WIN_PROB, pscl.LAST_STOCK_PRICE, pscl.BREAKEVEN_L, pscl.BREAKEVEN_H]]
                    display.sort_values([pscl.SYMBOL, pscl.STRATEGY],inplace=True)                        
                    display.columns  = [sub.replace('_', ' ') for sub in display.columns]                        
                    mail_body += '<h4>%s Contract # %d Max Risk $%.2f </h4>' % (account_name, symbol_option_position.shape[0],  max_risk)
                    mail_body += display.to_html(index=False)


        send_mail(app_settings.MY_GMAIL_USER,  
                    [to_addr], 
                    'Daily Account Satus Report!! ('+ ctime() + ') from ['+hostname+']', 
                    "Account Status for " + self.user_name ,
                    mail_body,      
                    files)
     
    def send_account_history_report(self):

        to_addr = self.get_user_email()

        from time import ctime

        from option_trader.utils.gmail_notify import send_mail 
        import option_trader.consts.strategy as st
        from option_trader.consts import asset

        from  option_trader.entity import position_summary
        import socket

        hostname = socket.gethostname()  

        account_list = self.get_account_list()

        if len(account_list)== 0:
            return

        history_df = pd.DataFrame()

        position_df = pd.DataFrame()

        for account_name in account_list:
            acct = self.get_account(account_name)
            acct.create_daily_account_summary()            
            init_balance = acct.get_initial_balance()
            d = acct.get_account_history().tail(1)
            e = acct.get_position_summary(status=asset.CLOSED)
            e.insert(0, 'account name', account_name)
            d.insert(0, 'account name', account_name) 
            d.at[d.index[0], 'Gain %'] =  round(100 * (d.at[d.index[0], 'account value'] - init_balance)/ init_balance, 2)       
            history_df = pd.concat([history_df, d])
            position_df = pd.concat([position_df, e])

        history_summary = history_df[['account name', 'account value', 'asset value', 'cash position', 'margin position', 'Profit/Loss', 'Gain %' ]]

        mail_body = "<h3>Account Summary</h3>" + history_summary.to_html(index=False)

        monitor_df = self.site.get_monitor_df()[['symbol', 'last_price', '10d change%', '10d low', '10d high', 'IV1%', 'earning']]

        monitor_df['dist. to 10d high'] = monitor_df.apply(lambda x: (x['10d high']-x['last_price']) / (x['10d high']-x['10d low']), axis = 1) 

        stock_position = position_df[position_df[pscl.STRATEGY] == st.UNPAIRED]
        if stock_position.shape[0] > 0:            
            mail_body += '<h3>Closed Stock Positions</h3>'            
            account_list = stock_position['account name'].unique()                    
            for account_name in account_list:
                act= stock_position[stock_position['account name']==account_name]
                stock_summary = act[[pscl.SYMBOL, pscl.QUANTITY, pscl.TRADE_DATE, pscl.STOP_DATE, pscl.OPEN_PRICE, pscl.LAST_STOCK_PRICE,  pscl.STOP_REASON,  pscl.GAIN, pscl.PL]]
                stock_summary.columns  = [sub.replace('_', ' ') for sub in stock_summary.columns]
                mail_body += '<h3>'+account_name+'</h3>'+stock_summary.to_html(index=False) 

        position_df['days opened'] = position_df.apply(lambda x: (pd.Timestamp(x[pscl.STOP_DATE]).date()-pd.Timestamp(x[pscl.TRADE_DATE]).date()).days, axis = 1)  

        position_df['days to expire'] = position_df.apply(lambda x: (pd.Timestamp(x[pscl.EXP_DATE]).date()-pd.Timestamp(x[pscl.TRADE_DATE]).date()).days, axis = 1)  

        position_df['stop trigger'] = position_df.apply(lambda x: (x['stop_reason'][0:9]), axis = 1) 
        
        position_df['hit target'] = position_df.apply(lambda x: (x['last_stock_price'] >= x['target_low']) & (x['last_stock_price'] <= x['target_high']), axis=1)
        
        position_df['under target'] = position_df.apply(lambda x: (x['last_stock_price'] < x['target_low']), axis=1)

        position_df['above target'] = position_df.apply(lambda x: (x['last_stock_price'] > x['target_high']), axis=1)

        option_position = position_df[position_df[pscl.STRATEGY] != st.UNPAIRED] 
        option_position[pscl.TRADE_STOCK_PRICE] = round(option_position[pscl.TRADE_STOCK_PRICE], 2)

        
        if option_position.shape[0] > 0:
            mail_body += '<h3>Closed Option Positions</h3>'            
            exp_date_list = option_position[pscl.EXP_DATE].unique()
            exp_date_list.sort()
            for exp_date in exp_date_list:           
                #option_summary = option_position[option_position[pscl.EXP_DATE]==exp_date]
                option_summary = option_position[option_position[pscl.EXP_DATE]==exp_date][['account name',pscl.SYMBOL, pscl.STRATEGY, 'days opened', pscl.GAIN, pscl.PL, pscl.STOP_REASON]]
                tc = option_summary.shape[0]
                wc = option_summary[option_summary[pscl.GAIN] > 0].shape[0]
                wrt = round(100*wc/tc,2)
                option_summary.sort_values(pscl.GAIN, inplace=True)
                option_summary.columns  = [sub.replace('_', ' ') for sub in option_summary.columns]                
                title = "%s trx %d win %d win rate:%.2f PL %.2f" %(exp_date, tc, wc, wrt, option_summary[pscl.PL].sum())
                mail_body += '<h3>'+title+'</h3>' #+ option_summary.to_html(index=False)

        files = []

        import tempfile

        report_path = os.path.join(tempfile.gettempdir(), 'trade_history_report.csv')

        position_df.to_csv(report_path, index=False)

        files.append(report_path)
                
        send_mail(app_settings.MY_GMAIL_USER, 
                    [to_addr], 
                    'Daily Account Historical Performance Report!! ('+ ctime() + ') from ['+hostname+']', 
                    "Account Status for " + self.user_name ,
                    mail_body,      
                    files)
                    
            
        return option_position

    from option_trader.utils.data_getter_ib import ib_daily_account_summary_col_name
    from option_trader.utils.data_getter_ib import ib_exceution_details_col_name
    from option_trader.utils.data_getter_ib import ib_completed_order_col_name


    def syncup_brokerage_accounts(self):

        brokerage = self.get_brokerage()
        if brokerage == None:
            return

        if 'IB' in brokerage:

            from option_trader.utils.data_getter_ib import load_ib_completedOrders
            from option_trader.utils.data_getter_ib import refresh_ib_open_orders 
            from option_trader.utils.data_getter_ib import load_ib_execution_details
            from option_trader.utils.data_getter_ib import refresh_ib_accounts_values_protfolio
            from option_trader.utils.data_getter_ib import load_ib_account_summary
            from option_trader.utils.data_getter_ib import refresh_ib_accounts_positions            

            from option_trader.settings import ib_settings

            live = False if 'PAPER' in brokerage else True   

            summary_dict = load_ib_account_summary(TWS=ib_settings.TWS, Live=live)
            if len(summary_dict.keys()) == 0:
                self.logger.warning('NO ACCOUNT LOADED')
                return
            else:
                for account_name in summary_dict.keys():
                    a = self.get_account(account_name)
                    a.save_ib_daily_account_summary(summary_dict[account_name])  

            account_name_list = summary_dict.keys()

            position_df = refresh_ib_accounts_positions(TWS=ib_settings.TWS, Live=live)            
            for account_name in account_name_list:  
                a = self.get_account(account_name)
                if position_df.shape[0] > 0:                
                    a.save_ib_account_positions(position_df[position_df['account']==account_name])
                else:
                    a.drop_ib_account_positions()    

            openOrder_df = refresh_ib_open_orders(TWS=ib_settings.TWS, live=live)
            for account_name in account_name_list:
                a = self.get_account(account_name)
                if openOrder_df.shape[0] > 0:                
                    a.save_ib_account_openOrders(openOrder_df[openOrder_df['account']==account_name])
                else:
                    a.drop_ib_account_openOrders()                    
                    
            v, p = refresh_ib_accounts_values_protfolio(TWS=ib_settings.TWS, Live=live)
            for account_name in account_name_list:
                a = self.get_account(account_name)
                if p.shape[0] > 0:                    
                    a.save_ib_account_portfolio(p[p['accountName']==account_name])
                else:
                    a.drop_ib_account_portfolio()                        

            for account_name in account_name_list:
                a = self.get_account(account_name)              
                a.save_ib_account_values(v[account_name])

            exec_defails_df = load_ib_execution_details(TWS=ib_settings.TWS, Live=live)
            for account_name in account_name_list:
                a = self.get_account(account_name)
                if exec_defails_df.shape[0] > 0:                    
                    a.save_ib_execution_details(exec_defails_df[exec_defails_df['acctNumber']==account_name])                           
                   
            try:
                completed_order_df = load_ib_completedOrders(TWS=ib_settings.TWS, Live=live)
                for account_name in account_name_list:
                    a = self.get_account(account_name)
                    if completed_order_df.shape[0] > 0:                    
                        a.save_ib_completed_orders(completed_order_df[completed_order_df['account']==account_name]) 

            except Exception as e:
                self.logger.exception(e)
                pass
            
if __name__ == '__main__':

    from option_trader.admin.user import user              
    from option_trader.admin.site import site        
    from option_trader.consts import strategy as st

    mlist =['AAPL','MSFT','NVDA','TSLA','ADBE','NFLX','QCOM','SHOP','ERF',
            'ABNB','ABT','AMAT','AMD','AMZN','ASML','AVGO','BA','BAC','BKNG',
            'CMG','COST','CRM','CUK','DOCU','DPZ','ETSY','F','FTNT','GOOGL',
            'ILMN','ISRG','KLAC','MCD','LRCX','MEDP','META','MRVL','MU','NKE',
            'ORCL','PANW','PFE','PLTR','PLUG','PYPL','QQQ','SPY','ROKU','RSG',
            'SBUX','SNOW','SQ','SWKS','TGT','TMO','TSM','TWLO','TXN','UPST',
            'VEEV','WMT', 'BLDR', 'TQQQ', 'V', 'JNJ', "NVDA", "AMD", "TSM", 
            "SMCI", "INTC", "SIMO","NXPI","AMBA","WDC","STX","ASX","EWBC","AAOI"]

    win_strategy = [st.WEEKLY_STOCK_TRADE, st.COVERED_CALL, st.SHORT_PUT, st.CREDIT_PUT_SPREAD, st.CREDIT_IRON_CONDOR, st.IRON_BUTTERFLY, st.CREDIT_PUT_BUTTERFLY]

    favorite = ['MSFT', 'AAPL', 'AMZN', 'NVDA', 'BLDR', 'COST', 'GOOGL', 'NFLX', 'META', 'AMD', 'ISRG', 'TSM', 'PLTR', 'CUK', 'TSLA', 'ISRG', 'PANW']

    mysite = site('mysite')

    paper = mysite.get_user('ib_user_paper')
    paper.syncup_brokerage_accounts()

    #live = mysite.get_user('ib_user_live')
    #live.syncup_brokerage_accounts()

    exit(0)

    mysite.update_default_watchlist(mlist)

    exit(0)
    
    ib_user = mysite.create_user('ib_user',
                                email='jim.huang.bellevue@gmail.com', 
                                watchlist=mlist,
                                strategy_list=win_strategy) 

    ib_user.create_account('U11370821',
                        initial_balance=500,
                        watchlist=favorite,
                        strategy_list=[st.WEEKLY_STOCK_TRADE])

    #chrishua = mysite.create_user('chrishua',
    #                            email='chrishua123@hotmail.com', 
    #                            watchlist=mlist,
    #                            strategy_list=win_strategy) 
    
    #user_name_list = mysite.get_user_list()
    #user_name_list = ['stester']
    #for user_name in user_name_list:        
    #    me = user(site=mysite, user_name=user_name)
    #    me.send_account_status_report()
    me = user(site=mysite, user_name='jihuang')
    me.send_account_status_report()    
    #me.update_account('weekly_trade')
    #me.update_account('spread')