import pandas as pd
import yfinance as yf
from yahoo_fin.options import *         

from datetime import time, date, datetime, timedelta

import pandas_market_calendars as mcal

import pytz
from pytz import timezone

import numpy as np
import math

from option_trader.consts import asset as at
from option_trader.settings import app_settings


from option_trader.utils.option_tool import delta_call
from option_trader.utils.option_tool import delta_put
from option_trader.utils.option_tool import theta_call
from option_trader.utils.option_tool import theta_put
from option_trader.utils.option_tool import gamma
from option_trader.utils.option_tool import vega

from option_trader.utils.option_tool import time_to_maturity_in_year
from option_trader.utils.calc_prob   import calc_win_prob
import option_trader.consts.strategy  as st
from  option_trader.entity.position_summary import position_summary_col_name as pscl
from  option_trader.entity.position import position_col_name as pcl
from  option_trader.entity import quote


import logging

import warnings

from pandas.errors import SettingWithCopyWarning

warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

            
from diskcache import Cache

cache = Cache()

def get_price_history(symbol, period='6mo', interval='1d'):     
    logger = logging.getLogger(__name__)    
    cache_key = symbol+'price_history'+period+interval
    if cache_key in cache:        
        try:
            h = cache[cache_key]       
            if h.shape[0] > 0:
                return h
        except:
            pass

    q = get_ticker(symbol)

    try:        
        hist = q.history(period=period, interval=interval)
        if hist.shape[0] > 0:
            cache.set(cache_key, hist, expire=300)
        else:
            logger.error('Cannot get quote for %s' % symbol)
        return hist              
    except Exception as ex:
        logger.exception('q.history raise exception %s' % symbol)
        raise ex
    
def get_ticker(symbol):
    return yf.Ticker(symbol) 
          
def get_last_dividend(symbol):
    cache_key = symbol+'last_dividend'
    if cache_key in cache:
        if cache_key in cache:
            try:
                return cache[cache_key]    
            except:
                pass            
   
    stock = get_ticker(symbol)
    ed = stock.get_dividends()
    if len(ed) > 0:
        cache.set(cache_key, ed, expire=86400)           
        return ed[-1]
    else:
        return 0.0      

def afterHours(now = None):

    import pandas_market_calendars as mcal
    from datetime import datetime

    tz = pytz.timezone(app_settings.TIMEZONE)
    #us_holidays = holidays.US()        
    if not now:
        now = datetime.now(tz)        
    openTime = time(hour = 9, minute = 30, second = 0)
    closeTime = time(hour = 16, minute = 0, second = 0)
    # If a holiday
    def market_is_open(date):
        result = mcal.get_calendar("NYSE").schedule(start_date=date, end_date=date)
        return result.empty == False
    
    # check if market was open 2023-04-16 (False)
    if market_is_open(now.strftime('%Y-%m-%d')) == False:
        return True

    # If before 0930 or after 1600
    if (now.time() < openTime) or (now.time() > closeTime):
        return True
    # If it's a weekend
    if now.date().weekday() > 4:
        return True

    return False       
    
def get_next_earning_date(symbol):
    cache_key = symbol+'next_earning_dates'
    if cache_key in cache:      
        try:
            return cache[cache_key]    
        except:
            pass         
    stock = get_ticker(symbol)
    ed = stock.get_earnings_dates()
    if isinstance(ed, type(None)):
        return None
    
    if ed.empty == False:
        today = pd.Timestamp.now(ed.head(1).index.tz)
        et = ed[ed.index > today]
        if et.empty == False:
            cache.set(cache_key, et.index[-1], expire=86400)        
            return et.index[-1]
    return None
        
def get_earning_dates(symbol):
    
    cache_key = symbol+'earning_dates'
    
    if cache_key in cache:      
        try:
            return cache[cache_key]    
        except:
            pass           
        
    stock = get_ticker(symbol)

    earning_dates = stock.get_earnings_dates()

    cache.set(cache_key, earning_dates, expire=86400)
    
    return earning_dates     

def get_support_resistence_levels(symbol, data=pd.DataFrame()):

    def isSupport(df,i):
        support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
        return support

    def isResistance(df,i):
        resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
        return resistance

    if data.empty:
        df = get_price_history(symbol)
    else:
        df = data

    s =  np.mean(df['High'] - df['Low'])

    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0

    SUPPORT = 0
    RESISTANCE = 1
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['Low'][i]
            if isFarFromLevel(l):
                levels.append((i,l,SUPPORT))
        elif isResistance(df,i):
            l = df['High'][i]
            if isFarFromLevel(l):
                levels.append((i,l,RESISTANCE))        

    l = range( len(levels) - 1, -1, -1)
    support = None
    resistence = None

    for i in l:
        if levels[i][2] == SUPPORT and support == None:
            support = levels[i][1]
        if levels[i][2] == RESISTANCE and resistence == None:
            if support != None and levels[i][1] > support:
                resistence = levels[i][1]

    return support, resistence

def get_option_exp_date(symbol, min_days_to_expire=app_settings.MIN_DAYS_TO_EXPIRE, max_days_to_expire=app_settings.MAX_DAYS_TO_EXPIRE):

    logger = logging.getLogger('get_option_exp_date')

    cache_key =symbol+'exp_date'+str(min_days_to_expire)+str(max_days_to_expire)
    if cache_key in cache:      
        try:
            return cache[cache_key]    
        except:
            pass   

    today = datetime.now(timezone(app_settings.TIMEZONE))

    q = get_ticker(symbol)        

    exp_date_list = q.options

    if len(exp_date_list) == 0:
        logger.debug("Cannot find exp dates for %s via yfinance, try yahoo_fin instead" % symbol)    
        from yahoo_fin import options
        xlist = options.get_expiration_dates(symbol)
        exp_date_list = [datetime.strptime(x, '%B %d, %Y').strftime('%Y-%m-%d') for x in xlist]
    
    list_to_return = []

    for exp_date in exp_date_list:        

        days_to_expire = (pd.Timestamp(exp_date).tz_localize(timezone(app_settings.TIMEZONE))-today).days+1

        if days_to_expire <= 0:
            continue

        if np.isnan(min_days_to_expire) == False:
            if days_to_expire < min_days_to_expire:
                continue

        if np.isnan(max_days_to_expire) == False:        
            if days_to_expire > max_days_to_expire:
                continue

        list_to_return.append(exp_date)

    cache.set(cache_key, list_to_return, expire=86400)    

    return list_to_return
    
def convert_yahoo_df(df):

    if 'contractSymbol' in df.columns:
        # yfinance 
        df.drop(['contractSymbol', 'lastTradeDate','change', 'currency', 'contractSize', 'inTheMoney', 'percentChange'], axis=1, inplace=True)

    if 'open interest' in df.columns:
        # yahoo_fin
        df.rename(columns={'last price':quote.LAST_PRICE, 'open interest': quote.OPEN_INTEREST, 'implied volatility': quote.IMPLIED_VOLATILITY}, inplace=True)
        df[quote.OPEN_INTEREST].replace(['-'], 0)

        #df.loc[df[quote.OPEN_INTEREST] == '-', quote.OPEN_INTEREST] = 0        

    df[quote.BID_SIZE] = df[quote.ASK_SIZE] = df[quote.OPEN] = df[quote.HIGH] = np.nan
    df[quote.LOW] = df[quote.CLOSE] = df[quote.DELTA] = df[quote.GAMMA] = np.nan
    df[quote.VEGA] = df[quote.THETA] = df[quote.SIGMA] = np.nan        
    return df

def get_option_chain(symbol, 
                    otype,
                    max_strike_ratio=0.25,                    
                    exp_date_list = [], 
                    min_days_to_expire=np.nan,                      
                    max_days_to_expire=np.nan,                     
                    max_bid_ask_spread=np.nan,
                    min_open_interest=np.nan): 
    
    import traceback

    logger = logging.getLogger(__name__)   

    if  otype not in [at.CALL, at.PUT]:
        logger.error('Invaid option type %s given' % otype)
        return pd.DataFrame()

    if len(exp_date_list) == 0:
        exp_date_list = get_option_exp_date(symbol, min_days_to_expire=min_days_to_expire, max_days_to_expire=max_days_to_expire)            

    if len(exp_date_list) == 0:
        logger.error('No exp date found %s' %symbol, ' min_days=', min_days_to_expire, ' max_days=', max_days_to_expire)
        return pd.DataFrame()
                    
    all_chain = pd.DataFrame()

    today = datetime.now(timezone(app_settings.TIMEZONE)).date()

    stock_price = get_price(symbol)

    for exp_date in exp_date_list:                   

        days_to_expire = (pd.Timestamp(exp_date).date()-today).days

        chain_cache_key =symbol+otype+'_chain'+exp_date

        chain = pd.DataFrame()
        if chain_cache_key in cache:  
            try:
                chain = cache[chain_cache_key]  
            except:
                pass              

        #if isinstance(calls, pd.DataFrame) and isinstance(puts, pd.DataFrame):
        #    return calls, puts
        #
        # if afterHours() == False:
        #    ib = IBClient.get_client()
        #    if ib != None and ib.isconnected():
        #        calls, puts = IB_get_option_chain(symbol, exp_date, stock_price)
        #        if calls.shape[0] == 0 or puts.shape[0] == 0:
        #            logger.info('Cannot get option chain from IB, try Yahoo now')
        #        else:
        #            calls, puts = insert_option_quote_meta(calls, puts, exp_date)                  
        #            cache.set(call_chain_cache_key, calls, expire=300)                      
        #            cache.set(put_chain_cache_key, puts, expire=300) 
        #            insert_option_quote_meta(calls, puts, exp_date):    
        #            return [calls, puts]

        if chain.shape[0] == 0: # not in chache
            try:
                q = get_ticker(symbol)
                if otype == at.CALL:
                    chain = q.option_chain(exp_date).calls           
                else:
                    chain = q.option_chain(exp_date).puts       
                cache.set(chain_cache_key, chain, expire=300)                           
            except Exception as e:       
                logger.debug('%s %s option chain for %s not found via yfinance use yahoo_fin instead' %(symbol, otype, exp_date))                
                if otype == at.CALL:
                    chain = get_calls(symbol, exp_date)      
                else:
                    chain = get_puts(symbol, exp_date)    
                                        
                chain.columns = [x.lower() for x in chain.columns]

                cache.set(chain_cache_key, chain, expire=300)      

        if np.isnan(max_strike_ratio) == False:
            i =  chain.shape[0]
            chain = chain[(abs(chain[quote.STRIKE]-stock_price)/stock_price) < max_strike_ratio ]
            #print('%s %d -> %d %s filtered on strike ratio <= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, max_strike_ratio))
            logger.debug('%s %s %d -> %d %s filtered on strike ratio <= %.2f' % (symbol, otype, i, chain.shape[0], otype, max_strike_ratio))

        if chain.shape[0] == 0:
            continue
        
        chain = convert_yahoo_df(chain)      

        chain[quote.PRICE] = chain.apply(lambda x: (x[quote.BID] + x[quote.ASK]) / 2 if (x[quote.BID] + x[quote.ASK]) > 0 else  x[quote.LAST_PRICE], axis=1)

        chain[quote.BID_ASK_SPREAD] = (chain[quote.ASK] - chain[quote.BID])

        S = stock_price

        chain[quote.SYMBOL]   = symbol
        chain[quote.EXP_DATE] = exp_date
        if otype == at.CALL:
            chain[quote.OTYPE] = at.CALL
            chain[quote.DELTA] = chain.apply(lambda x: delta_call(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
            chain[quote.THETA] = chain.apply(lambda x: theta_call(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
            #chain[quote.BREAKEVEN_LONG] = chain.apply(lambda x: x[quote.STRIKE] + x[quote.PRICE], axis=1)
            #chain[quote.BREAKEVEN_SHORT] = chain.apply(lambda x: x[quote.STRIKE] - x[quote.PRICE], axis=1)
            #chain[quote.WIN_PROB_LONG] = chain.apply(lambda x: calc_prob_higher_than(predList, x[quote.BREAKEVEN_LONG]), axis=1)
            #chain[quote.WIN_PROB_SHORT] = chain.apply(lambda x: calc_prob_lower_than(predList, x[quote.BREAKEVEN_SHORT]), axis=1)
            chain[quote.IN_MONEY] = chain.apply(lambda x: stock_price - x[quote.STRIKE] , axis=1)
        else:
            chain[quote.OTYPE] = at.PUT
            chain[quote.DELTA] = chain.apply(lambda x: delta_put(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)                 
            chain[quote.THETA] = chain.apply(lambda x: theta_put(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
            #chain[quote.BREAKEVEN_LONG] = chain.apply(lambda x: x[quote.STRIKE] - x[quote.PRICE], axis=1)
            #chain[quote.BREAKEVEN_SHORT] = chain.apply(lambda x: x[quote.STRIKE] + x[quote.PRICE], axis=1)
            #chain[quote.WIN_PROB_LONG] = chain.apply(lambda x: calc_prob_lower_than(predList, x[quote.BREAKEVEN_LONG]), axis=1)
            #chain[quote.WIN_PROB_SHORT] = chain.apply(lambda x: calc_prob_higher_than(predList, x[quote.BREAKEVEN_SHORT]), axis=1)
            chain[quote.IN_MONEY] = chain.apply(lambda x: x[quote.STRIKE] - stock_price, axis=1)

        chain[quote.GAMMA] == chain.apply(lambda x: gamma(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
        chain[quote.VEGA] = chain.apply(lambda x: vega(S, x[quote.STRIKE], time_to_maturity_in_year(today, pd.Timestamp(x[quote.EXP_DATE]).date())),axis=1)
        chain[quote.STOCK_PRICE] = stock_price
        chain[quote.DAYS_TO_EXPIRE] = days_to_expire

        all_chain = pd.concat([all_chain, chain])

    #if math.isnan(max_price) != True:
    #    i =  chain.shape[0]
    #    chain = chain[chain[quote.PRICE] <= max_price]
        #print('%s %d -> %d %s filtered on max price <= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, max_price))
    #    logger.debug('%d -> %d %s filtered on max price <= %.2f' % (i, chain.shape[0], otype, max_price))

    chain = all_chain

    #if math.isnan(min_price) != True:
    #    i =  chain.shape[0]
    #    chain = chain[chain[quote.PRICE] >= min_price]
    #    #print('%s %d -> %d %s filtered out min price >= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, min_price))
    #    logger.debug('%d -> %d %s filtered on min price >= %.2f' % (i, chain.shape[0], otype, min_price))

    if chain.shape[0] == 0:
        return chain

    if np.isnan(max_bid_ask_spread) == False:
        i =  chain.shape[0]
        chain = chain[chain[quote.BID_ASK_SPREAD] < max_bid_ask_spread]
        #print('%s %d -> %d %s filtered on bid/ask spread <= %.2f' % (get_option_chain.__name__, i, chain.shape[0], otype, max_bid_ask_spread))
        logger.debug('%s %s %d -> %d %s filtered on bid/ask spread < %.2f' % (symbol, otype, i, chain.shape[0], otype, max_bid_ask_spread))

    '''
    if np.isnan(min_open_interest) == False:
        print('xxx', chain[quote.OPEN_INTEREST].max())
        i = chain.shape[0]
        chain = chain[chain[quote.OPEN_INTEREST].astype(int) > min_open_interest]
        #print('%s %d -> %d %s filtered on openInteretst >= %d' % (get_option_chain.__name__, i, chain.shape[0], otype, min_open_interest))
        logger.debug('%s %d -> %d %s filtered on openInterest > %d' % (symbol, i, chain.shape[0], otype, min_open_interest))
    '''
    return chain

def get_option_leg_IV_delta(symbol, exp_date, otype):
 
    logger = logging.getLogger(__name__)

    trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date()     
 
    stock_price = get_price(symbol)

    q = get_ticker(symbol)

    if otype == at.CALL:
        opt = q.option_chain(exp_date).calls    
    else:
        opt = q.option_chain(exp_date).puts    

    leg = opt[opt[quote.STRIKE] >= stock_price]  

    if leg.shape[0] > 0:         
        iv =  round(leg[quote.IMPLIED_VOLATILITY].head(1).values[0],3)
        strike = leg[quote.STRIKE].head(1).values[0]
        T = time_to_maturity_in_year(trade_date, exp_date)        
        if T == 0:
            logger.error('T==0 trade date %s exp_date%s' % (str(trade_date), exp_date))
            delta = np.nan
        else:
            delta = delta_call(stock_price, strike, T)    
        return iv, delta
    else:
        return np.nan, np.nan
        
def get_IV_geeks(symbol, stock_price, exp_date, strike):
    logger = logging.getLogger(__name__)   

    geeks_key =symbol+'geeks_leg'+str(strike)+exp_date
    if geeks_key in cache:
        return cache[geeks_key]
    
    '''
    if afterHours() == False:    
        ib = IBClient.get_client()
        if ib != None:
            x = IB_get_option_leg_details(symbol, exp_date, strike, otype) 
            if x == None:
                logger.debug("Failed to get option quote from IB, try yahoo next")
            else:        
                cache.set(option_leg_key, x, expire=300)                            
                return x
    '''        
    geeks = {'iv': np.nan,
             'call_delta': np.nan,
             'call_theta': np.nan,
             'put_delta': np.nan,
             'put_theta': np.nan,
             'gamma' : np.nan,
             'vega' : np.nan}

    trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date()
    T = time_to_maturity_in_year(trade_date, exp_date)
    q = get_ticker(symbol)
    calls = q.option_chain(exp_date).calls            
    call_leg = calls[calls[quote.STRIKE] >= strike]         
    if call_leg.shape[0] > 0:         
        geeks['iv'] =  round(call_leg[quote.IMPLIED_VOLATILITY].head(1).values[0],3)
        strike = call_leg[quote.STRIKE].head(1).values[0] 
        geeks['call_delta'] = delta_call(stock_price, strike, T)
        geeks['call_theta'] = theta_call(stock_price, strike, T)
        geeks['gamma']      = gamma(stock_price, strike, T)   
        geeks['vega']       = vega(stock_price, strike, T)          

    puts = q.option_chain(exp_date).puts  
    put_leg = puts[puts[quote.STRIKE] >=strike]        
    if put_leg.shape[0] > 0:         
        if np.isnan(geeks['iv']):
            geeks['iv'] = round(put_leg[quote.IMPLIED_VOLATILITY].head(1).values[0],3)
        strike = put_leg[quote.STRIKE].head(1).values[0] 
        geeks['put_delta'] = delta_put(stock_price, strike, T)
        geeks['put_theta'] = theta_put(stock_price, strike, T)
        if np.isnan(geeks['gamma']):
            geeks['gamma'] = gamma(stock_price, strike, T)          
        if np.isnan(geeks['vega']):
            geeks['vega'] = vega(stock_price, strike, T)          
            
    cache.set(geeks_key, geeks, expire=300)         
    return geeks            

def get_option_leg_details(symbol, stock_price, exp_date, strike, otype):

    logger = logging.getLogger(__name__)   

    option_leg_key =symbol+'option_leg'+str(strike)+otype+exp_date
    #logger.info(option_leg_key)
    if option_leg_key in cache:
        return cache[option_leg_key]
    
    '''
    if afterHours() == False:    
        ib = IBClient.get_client()
        if ib != None:
            x = IB_get_option_leg_details(symbol, exp_date, strike, otype) 
            if x == None:
                logger.debug("Failed to get option quote from IB, try yahoo next")
            else:        
                cache.set(option_leg_key, x, expire=300)                            
                return x
    '''        
    trade_date = datetime.now().astimezone(timezone(app_settings.TIMEZONE)).date()

    T = time_to_maturity_in_year(trade_date, exp_date)
    
    q = get_ticker(symbol)

    if otype == at.CALL:
        cache_key =symbol+'call_chain'+exp_date               
        calls = pd.DataFrame() 
        if cache_key in cache:
            try:
                calls = cache[cache_key]
            except:
                pass            
        
        if calls.shape[0] == 0:
            calls = q.option_chain(exp_date).calls         
            cache.set(cache_key, calls, expire=300)                 
        
        calls[quote.EXP_DATE] = exp_date
        leg = calls[calls[quote.STRIKE]==strike]             
        if leg.shape[0] == 0:
            logger.error('cannot find leg detail %s %s %.1f %s' % (symbol, exp_date, strike, otype))            
            return {}       

        leg = convert_yahoo_df(leg)           
        leg = leg.to_dict('records')[0]                       
        if T > 0:
            leg[quote.DELTA] = delta_call(stock_price, strike, T)
            leg[quote.THETA] = theta_call(stock_price, strike, T)
            leg[quote.GAMMA] = gamma(stock_price, strike, T)
            leg[quote.VEGA]  = vega(stock_price, strike, T)
        else:
            leg[quote.DELTA] = leg[quote.THETA] = leg[quote.GAMMA] = leg[quote.VEGA]  = np.nan

    elif otype == at.PUT:
        cache_key =symbol+'put_chain'+exp_date          
        
        puts = pd.DataFrame()
        if cache_key in cache:
            try:
                puts = cache[cache_key]
            except:
                pass            
        
        if puts.shape[0] == 0: 
            puts = q.option_chain(exp_date).puts        
            cache.set(cache_key, puts, expire=300) 

        puts[quote.EXP_DATE] = exp_date
        leg = puts[puts[quote.STRIKE]==strike]
        if leg.shape[0] == 0:
            logger.error('cannot find leg detail %s %s %.1f %s' % (symbol, exp_date, strike, otype))            
            return {}           
        leg = convert_yahoo_df(leg)   
        leg = leg.to_dict('records')[0]    
        if T > 0:
            leg[quote.DELTA] = delta_put(stock_price, strike, T)
            leg[quote.THETA] = theta_put(stock_price, strike, T)
            leg[quote.GAMMA] = gamma(stock_price, strike, T)
            leg[quote.VEGA]  = vega(stock_price, strike, T)        
        else:
            leg[quote.DELTA] = leg[quote.THETA] = leg[quote.GAMMA] = leg[quote.VEGA]  = np.nan
    else:
        logger.error('invalie otype %s %s %.1f %s' % (symbol, exp_date, strike, otype))            
        return {}
    
    cache.set(option_leg_key, leg, expire=300)         

    return leg            
 
def pick_option_long( symbol, 
                      otype,                   
                      predictlist,
                      max_strike_ratio=0.25,           
                      min_pnl = 0.25,                                             
                      min_win_prob=0.2,
                      max_bid_ask_spread=np.nan,
                      min_open_interest=0):

    logger = logging.getLogger(__name__)   

    if  otype not in [at.CALL, at.PUT]:
        logger.error('Invaid option type %s given' % otype)
        return pd.DataFrame()

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            otype,                         
                            exp_date_list= exp_date_list,                            
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    if chain.shape[0] == 0:
        return pd.DataFrame()

    single_df = pd.DataFrame()    

    stock_price = get_price(symbol)

    for exp_date in exp_date_list:  
        target_low = predictlist[exp_date][quote.LOW]      
        target_high = predictlist[exp_date][quote.HIGH]                     
        if otype == at.CALL:              
            calls = chain[(chain[quote.STRIKE] < stock_price) & (chain[quote.EXP_DATE]==exp_date)] 
            calls.sort_values(by=[quote.STRIKE], ascending = False, inplace=True)
            for i, call in calls.iterrows():                           
                df = create_single_df(call, stock_price, target_high, target_low, credit=False)
                if df.shape[0] > 0:
                    if df.at[0, pscl.PNL] < min_pnl:
                        break              
                    single_df = pd.concat([single_df, df])
        elif otype == at.PUT:               
            puts = chain[(chain[quote.STRIKE] > stock_price) & (chain[quote.EXP_DATE]==exp_date)]
            puts.sort_values(by=[quote.STRIKE], inplace=True)            
            for i, put in puts.iterrows():                         
                df = create_single_df(put, stock_price, target_high, target_low, credit=False)
                if df.shape[0] > 0:
                    if df.at[0, pscl.PNL] < min_pnl:
                        break                  
                    single_df = pd.concat([single_df, df])

    if single_df.shape[0] == 0:
        return pd.DataFrame()
    
    win_prob_range = '[%.2f|%.2f]' % (single_df[pscl.WIN_PROB].min(), single_df[pscl.WIN_PROB].max())
    i = single_df.shape[0]
    single_df= single_df[single_df[pscl.WIN_PROB] >= min_win_prob]
    #print('%s %d -> %d fillterd out by win prob >= %.2f' % (inspect.currentframe().f_code.co_name, i, spread_df.shape[0], min_win_prob))
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, single_df.shape[0], min_win_prob, win_prob_range))

    if otype == at.PUT:
        i = single_df.shape[0]         
        singl_df = single_df[(single_df[pscl.BREAKEVEN_H]/single_df[pscl.TARGET_HIGH]) > 1.01]
        logger.debug('%d -> %d reduced by h/high > 1.0' % (i, single_df.shape[0]))

    '''
    [lp h/high>1.00] [69.23%|18|8]	[2292.06|-1421.75]	96.30%
        HIT	 [63.64%|14|8]	[1378.71|-1421.75]	51.85%
        UNDER	 [100.00%|4|0]	[5488.75|nan]	14.81%
    '''    

    if otype == at.CALL:
        i = single_df.shape[0]          
        singl_df = single_df[(single_df[pscl.BREAKEVEN_L]/single_df[pscl.TARGET_LOW]) < 1.03]
        logger.debug('%d -> %d reduced by l/low < 1.03' % (i, single_df.shape[0]))
    '''
    [lc l/low<1.03] [66.67%|14|7]	[1307.57|-347.00]	36.84%
        HIT	 [83.33%|10|2]	[1210.50|-283.50]	17.54%
        UNDER	 [16.67%|1|5]	[58.00|-372.40]	1.75%
        ABOVE	 [100.00%|3|0]	[2047.67|nan]	5.26%
    '''

    return single_df

def pick_option_short( symbol, 
                      otype,                   
                      predictlist,
                      min_pnl = 0.25,
                      min_price = 1.0,
                      max_strike_ratio=0.25,                             
                      min_win_prob=0.2,
                      max_bid_ask_spread=np.nan,
                      min_open_interest=0):

    logger = logging.getLogger(__name__)   

    if  otype not in [at.CALL, at.PUT]:
        logger.error('Invaid option type %s given' % otype)
        return pd.DataFrame()

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            otype,                         
                            exp_date_list= exp_date_list,                            
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    if chain.shape[0] == 0:
        return pd.DataFrame()

    single_df = pd.DataFrame()    

    stock_price = get_price(symbol)

    for exp_date in exp_date_list:  
        target_low = predictlist[exp_date][quote.LOW]      
        target_high = predictlist[exp_date][quote.HIGH]      
        if otype == at.CALL:              
            calls = chain[(chain[quote.STRIKE] > stock_price) & (chain[quote.EXP_DATE]==exp_date)]
            calls.sort_values(by=[quote.STRIKE], inplace=True)                
            for i, call in calls.iterrows():       
                df = create_single_df(call, stock_price, target_high, target_low, credit=True)
                if df.shape[0] > 0:
                    if df.at[0, pscl.PNL] < min_pnl:
                        break                  
                    single_df = pd.concat([single_df, df])
        elif otype == at.PUT:                
            puts = chain[(chain[quote.STRIKE] < stock_price) & (chain[quote.EXP_DATE]==exp_date)]
            puts.sort_values(by=[quote.STRIKE], ascending = False, inplace=True)                
            for i, put in puts.iterrows():                   
                df = create_single_df(put, stock_price, target_high, target_low, credit=True)
                if df.shape[0] > 0:
                    if df.at[0, pscl.PNL] < min_pnl:
                        break                       
                    single_df = pd.concat([single_df, df])

    if single_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (single_df[pscl.OPEN_PRICE].min(), single_df[pscl.OPEN_PRICE].max())
    i = single_df.shape[0]
    single_df= single_df[single_df[pscl.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, single_df.shape[0], min_price, open_price_range))

    win_prob_range = '[%.2f|%.2f]' % (single_df[pscl.WIN_PROB].min(), single_df[pscl.WIN_PROB].max())
    i = single_df.shape[0]
    single_df= single_df[single_df[pscl.WIN_PROB] >= min_win_prob]
    logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, single_df.shape[0], min_win_prob, win_prob_range))
    
    if otype == at.PUT:
        i = single_df.shape[0]         
        singl_df = single_df[single_df[pscl.BREAKEVEN_H] < single_df[pscl.TARGET_LOW]]
        logger.debug('%d -> %d reduced by h < low' % (i, single_df.shape[0]))
    if otype == at.CALL:
        i = single_df.shape[0]              
        singl_df = single_df[single_df[pscl.BREAKEVEN_L] > single_df[pscl.TARGET_HIGH]]
        logger.debug('%d -> %d reduced by l > high' % (i, single_df.shape[0]))

    return single_df

def pick_vertical_put_spreads( symbol,                          
                                predictlist,
                                credit=True,
                                max_spread = 10,
                                max_strike_ratio=0.25,
                                min_pnl=0.2,                                
                                min_win_prob=np.nan,
                                max_bid_ask_spread=np.nan,
                                min_open_interest=0):

    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    puts = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list= exp_date_list,                               
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)     
    
    spread_df = pd.DataFrame()        

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        tputs = puts[ (puts[quote.STRIKE]  >= target_low ) &
                        (puts[quote.STRIKE]  <= target_high ) &
                        (puts[quote.EXP_DATE]==exp_date)]        

        if tputs.shape[0] == 0:
            continue

        if credit:    
            for i, sleg in tputs.iterrows():       
                tlputs = puts[(puts[quote.STRIKE]   <   sleg[quote.STRIKE]) &
                              (puts[quote.STRIKE]   >=  sleg[quote.STRIKE]-max_spread) &
                              (puts[quote.EXP_DATE] ==  exp_date)]  

                if tlputs.shape[0] == 0:
                    logger.debug('Cannot find long legs for %s %.2f' % (str(sleg[quote.EXP_DATE]), sleg[quote.STRIKE]))
                    continue            

                tlputs.sort_values(quote.STRIKE, ascending=False, inplace=True)                                     
                for j, lleg in tlputs.iterrows():                                             
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.PUT) 
                    if df.shape[0] > 0:
                        spread_df = pd.concat([spread_df, df])
        else:
            for i, lleg in tputs.iterrows():

                sputs = puts[(puts[quote.STRIKE]   <   lleg[quote.STRIKE]) &
                             (puts[quote.STRIKE]   >=  lleg[quote.STRIKE]-max_spread) &
                             (puts[quote.EXP_DATE] ==  exp_date)]                  
                if sputs.shape[0] == 0:
                    logger.debug('Cannot find short legs for %s %.2f' % (str(lleg[quote.EXP_DATE]), lleg[quote.STRIKE]))
                    continue                                           

                for j, sleg in sputs.iterrows(): 
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.PUT, credit=False)                                                                             
                    if df.shape[0] > 0:
                        spread_df = pd.concat([spread_df, df])

    if spread_df.shape[0] > 0:

        if math.isnan(min_win_prob) == False:
            win_prob_range = '[%.2f|%.2f]' % (spread_df[pscl.WIN_PROB].min(), spread_df[pscl.WIN_PROB].max())
            i = spread_df.shape[0]
            spread_df= spread_df[spread_df[pscl.WIN_PROB] >= min_win_prob]
            logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, spread_df.shape[0], min_win_prob, win_prob_range))

        if math.isnan(min_pnl) == False:
            pnl_range = '[%.2f|%.2f]' % (spread_df[pscl.PNL].min(), spread_df[pscl.PNL].max())
            i = spread_df.shape[0]
            spread_df= spread_df[spread_df[pscl.PNL] >= min_pnl]
            logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, spread_df.shape[0], min_pnl, pnl_range))

        if credit:
            i =spread_df.shape[0]               
            spread_df = spread_df[(spread_df[pscl.BREAKEVEN_L]/spread_df[pscl.TARGET_LOW]) < 1.01]
            logger.debug('%d -> %d reduced by l/Low < 1.01' % (i, spread_df.shape[0]))
            '''
            [cps All] [37.68%|78|129]	[1133.42|-1376.46]	100.00%
                HIT	 [63.73%|65|37]	[1144.94|-1337.08]	31.40%
                UNDER	 [1.08%|1|92]	[390.00|-1392.29]	0.48%
                ABOVE	 [100.00%|12|0]	[1133.00|nan]	5.80%
            -------------------------------------------------------
            [cps l/low<1.01] [39.45%|43|66]	[1302.47|-1218.77]	52.66%
                HIT	 [95.12%|39|2]	[1337.64|-355.50]	18.84%
                UNDER	 [1.54%|1|64]	[390.00|-1245.75]	0.48%
                ABOVE	 [100.00%|3|0]	[1149.33|nan]	1.45%

            '''

        else:
            i =spread_df.shape[0]               
            spread_df = spread_df[(spread_df[pscl.BREAKEVEN_H]/spread_df[pscl.TARGET_HIGH]) > 0.97]
            logger.debug('%d -> %d reduced by h/high > 0.97' % (i, spread_df.shape[0]))
        '''
        [dps All] [60.00%|105|70]	[5574.44|-1652.89]	100.00%
            HIT	 [56.20%|68|53]	[6871.79|-1509.68]	38.86%
            UNDER	 [100.00%|37|0]	[3190.11|nan]	21.14%
            ABOVE	 [0.00%|0|17]	[nan|-2099.35]	0.00%
        -----------------------------------------
        [dps h/high > 0.97] [80.60%|54|13]	[7502.74|-1786.77]	38.29%
            HIT	 [90.24%|37|4]	[8736.24|-976.50]	21.14%
            UNDER	 [100.00%|17|0]	[4818.06|nan]	9.71%
            ABOVE	 [0.00%|0|9]	[nan|-2146.89]	0.00%
        '''            
    return spread_df
 
def pick_vertical_call_spreads(symbol,                          
                                predictlist,
                                credit=True,
                                max_spread = 10,
                                max_strike_ratio=0.25,
                                min_pnl=0.2,                                
                                min_win_prob=np.nan,
                                max_bid_ask_spread=np.nan,
                                min_open_interest=0):

    logger = logging.getLogger(__name__)   

    spread_df = pd.DataFrame()

    exp_date_list = predictlist['exp_date_list']

    calls = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list= exp_date_list,                               
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)    
    
    stock_price = get_price(symbol)

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    
        target_high = predictlist[exp_date][quote.HIGH]    

        tcalls = calls[ (calls[quote.STRIKE]  >= target_low ) &
                        (calls[quote.STRIKE]  <= target_high ) &
                        (calls[quote.EXP_DATE] == exp_date)]   
        
        if tcalls.shape[0] == 0:
            continue 
                
        if credit:                     
            tcalls.sort_values(quote.STRIKE,  ascending=False, inplace=True)        
            for i, sleg in tcalls.iterrows():   
                lcalls = calls[(calls[quote.STRIKE]   >   sleg[quote.STRIKE]) & 
                               (calls[quote.STRIKE]   <=  sleg[quote.STRIKE]+max_spread) &
                               (calls[quote.EXP_DATE] ==  sleg[quote.EXP_DATE])]

                if lcalls.shape[0] == 0:
                    logger.debug('Cannot find long legs for %s %.2f' % (str(sleg[quote.EXP_DATE]), sleg[quote.STRIKE]))
                    continue            
                lcalls.sort_values(quote.STRIKE, inplace=True)                            
                for j, lleg in lcalls.iterrows():
                    #print('long strike', lleg[quote.STRIKE])                                                       
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.CALL)      
                    if df.shape[0] > 0:
                        spread_df = pd.concat([spread_df, df])          
        else:                 
            for i, lleg in tcalls.iterrows():
                scalls = calls[ (calls[quote.STRIKE]   >   lleg[quote.STRIKE]) &
                                (calls[quote.STRIKE]   <=  lleg[quote.STRIKE]+max_spread) &
                                (calls[quote.EXP_DATE] ==  lleg[quote.EXP_DATE])]

                if scalls.shape[0] == 0:
                    logger.debug('Cannot find short legs for %s %.2f' % (str(lleg[quote.EXP_DATE]), lleg[quote.STRIKE]))
                    continue                                           

                for j, sleg in scalls.iterrows():                    
                    df = create_spread_df(target_low, target_high, sleg, lleg, at.CALL, credit=False)                                       
                    if df.shape[0] > 0:
                        spread_df = pd.concat([spread_df, df])



    if spread_df.shape[0] == 0:
        return pd.DataFrame()        
    

    if math.isnan(min_win_prob) == False:
        win_prob_range = '[%.2f|%.2f]' % (spread_df[pscl.WIN_PROB].min(), spread_df[pscl.WIN_PROB].max())
        i = spread_df.shape[0]
        spread_df= spread_df[spread_df[pscl.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, spread_df.shape[0], min_win_prob, win_prob_range))

    if math.isnan(min_pnl) == False:
        pnl_range = '[%.2f|%.2f]' % (spread_df[pscl.PNL].min(), spread_df[pscl.PNL].max())
        i = spread_df.shape[0]
        spread_df= spread_df[spread_df[pscl.PNL] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, spread_df.shape[0], min_pnl, pnl_range))

    if credit:
        i =spread_df.shape[0]               
        spread_df = spread_df[(spread_df[pscl.BREAKEVEN_H]/spread_df[pscl.TARGET_HIGH]) > 0.99]
        logger.debug('%d -> %d reduced by h/high > 0.99' % (i, spread_df.shape[0]))

    '''

    [ccs All] [66.54%|173|87]	[1101.96|-1347.02]	100.00%
        HIT	 [53.94%|89|76]	[995.01|-1329.24]	34.23%
        UNDER	 [98.80%|82|1]	[1236.51|-1692.00]	31.54%
        ABOVE	 [16.67%|2|10]	[344.50|-1447.70]	0.77%
    -----------------------------------------
    [ccs h/high>0.99] [83.02%|44|9]	[1160.09|-759.11]	20.38%
        HIT	 [88.89%|32|4]	[1176.28|-272.75]	12.31%
        UNDER	 [100.00%|10|0]	[1271.40|nan]	3.85%
        ABOVE	 [28.57%|2|5]	[344.50|-1148.20]	0.77%

    '''
    return spread_df

def pick_iron_condor(symbol,                                              
                    predictlist,
                    credit=True,                    
                    max_spread=10,
                    max_strike_ratio=0.25,                           
                    min_price=1.0,
                    min_pnl=0.2,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=0):

    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    put_chain = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    call_chain = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)


    iron_condor_df = pd.DataFrame()

    strategy = st.CREDIT_IRON_CONDOR if credit else st.DEBIT_IRON_CONDOR

    logger.debug('%s %s' %(symbol, strategy))

    for exp_date in exp_date_list:
        target_low = predictlist[exp_date][quote.LOW]      
        target_high = predictlist[exp_date][quote.HIGH]     
        target_mid = (target_low+target_high) / 2


        pha = put_chain[(put_chain[quote.STRIKE]   >= target_low ) &
                    (put_chain[quote.STRIKE]   <= target_mid) &
                    (put_chain[quote.PRICE]    >= min_price) &                        
                    (put_chain[quote.EXP_DATE] == exp_date)]              

        if pha.shape[0] == 0:
            continue    

        for i, ph in pha.iterrows():       

            pla = put_chain[(put_chain[quote.STRIKE]   <   ph[quote.STRIKE]) &
                            (put_chain[quote.STRIKE]   >=  ph[quote.STRIKE]-max_spread) &
                            (put_chain[quote.EXP_DATE] ==  exp_date)]  

            if pla.shape[0] == 0:
                continue

            for j, pl in pla.iterrows():    

                if  ph[quote.PRICE] <= pl[quote.PRICE]:
                    continue

                spread = ph[quote.STRIKE] - pl[quote.STRIKE]          
                cla =  call_chain[(call_chain[quote.EXP_DATE] == exp_date)  &
                                    (call_chain[quote.PRICE]  >= min_price) &                                  
                                    (call_chain[quote.STRIKE] > ph[quote.STRIKE])]  
                
                for k, cl in cla.iterrows():
                    cha = call_chain[(call_chain[quote.EXP_DATE] == exp_date)  &
                                        (call_chain[quote.STRIKE] == cl[quote.STRIKE]+spread)]  

                    if cha.shape[0] == 0:
                        continue              

                    for l, ch in cha.iterrows():

                        if  cl[quote.PRICE] <= ch[quote.PRICE]:       
                            continue      

                        df = create_iron_condor_df(strategy, target_low, target_high, pl=pl, ph=ph, cl=cl, ch=ch)              
                        if df.shape[0] > 0:
                            iron_condor_df = pd.concat([iron_condor_df, df])


    if iron_condor_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (iron_condor_df[pscl.OPEN_PRICE].min(), iron_condor_df[pscl.OPEN_PRICE].max())
    i = iron_condor_df.shape[0]
    iron_condor_df = iron_condor_df[iron_condor_df[pscl.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, iron_condor_df.shape[0], min_price, open_price_range))

    if math.isnan(min_win_prob) == False:
        win_prob_range = '[%.2f|%.2f]' % (iron_condor_df[pscl.WIN_PROB].min(), iron_condor_df[pscl.WIN_PROB].max())
        i = iron_condor_df.shape[0]
        iron_condor_df= iron_condor_df[iron_condor_df[pscl.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, iron_condor_df.shape[0], min_win_prob, win_prob_range))

    if math.isnan(min_pnl) == False:
        pnl_range = '[%.2f|%.2f]' % (iron_condor_df[pscl.PNL].min(), iron_condor_df[pscl.PNL].max())
        i = iron_condor_df.shape[0]
        iron_condor_df= iron_condor_df[iron_condor_df[pscl.PNL] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, iron_condor_df.shape[0], min_pnl, pnl_range))

    if credit:
        i =iron_condor_df.shape[0]               
        #iron_condor_df = iron_condor_df[((iron_condor_df[pscl.BREAKEVEN_L]/iron_condor_df[pscl.TARGET_LOW])<1.00) &  ((iron_condor_df[pscl.BREAKEVEN_H]/iron_condor_df[pscl.TARGET_HIGH]) > 0.98)]
        #logger.debug('%d -> %d reduced by l/low > 1.0 &  h/high > 0.98' % (i, iron_condor_df.shape[0]))

        '''
        [cic All] [56.12%|55|43]	[1131.60|-1226.33]	100.00%
            HIT	 [80.36%|45|11]	[1195.84|-802.36]	45.92%
            UNDER	 [8.82%|3|31]	[575.67|-1376.48]	3.06%
            ABOVE	 [87.50%|7|1]	[956.86|-1235.00]	7.14%
        ---------------l/low < x and h/high > y ----------------------
        [cic l/low <1.00 and h/high > 0.98] [54.84%|17|14]	[1980.41|-1259.36]	31.63%
            HIT	 [94.12%|16|1]	[2064.38|-16.00]	16.33%
            UNDER	 [7.14%|1|13]	[637.00|-1355.00]	1.02%
        '''
    else:
        #only puck expdate right after earning      
        i =iron_condor_df.shape[0]               
        #iron_condor_df = iron_condor_df[((iron_condor_df[pscl.BREAKEVEN_L]/iron_condor_df[pscl.TARGET_LOW])<1.03)]
        #logger.debug('%d -> %d reduced h/high > 1.03' % (i, iron_condor_df.shape[0]))
        '''
        [dic All] [52.31%|68|62]	[2297.72|-1171.69]	100.00%
            HIT	 [27.03%|20|54]	[1857.10|-1251.07]	15.38%
            UNDER	 [81.58%|31|7]	[1353.71|-724.43]	23.85%
            ABOVE	 [94.44%|17|1]	[4537.53|-16.00]	13.08%
        [dic l/low<1.03] [59.26%|16|11]	[3620.00|-1041.73]	20.77%
            HIT	 [25.00%|3|9]	[3574.33|-1092.67]	2.31%
            UNDER	 [83.33%|10|2]	[1050.50|-812.50]	7.69%
            ABOVE	 [100.00%|3|0]	[12230.67|nan]	2.31%
        '''
    return iron_condor_df

def pick_call_butterfly(symbol,                         
                    predictlist, 
                    spread_list=[],
                    credit=True,
                    max_spread=10,
                    max_strike_ratio=0.25,                             
                    min_price = np.nan,
                    min_pnl=np.nan,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=0):
    
    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    
    butterfly_df = pd.DataFrame()

    strategy = st.CREDIT_CALL_BUTTERFLY if credit else st.DEBIT_CALL_BUTTERFLY

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        target_price = (predictlist[exp_date][quote.HIGH]+predictlist[exp_date][quote.LOW])/2

        mall = chain[(abs(chain[quote.STRIKE]-target_price) < 2.5)]

        if mall.shape[0] == 0:
            continue

        mexp = mall[mall[quote.EXP_DATE]==exp_date]
        if mexp.shape[0] == 0:
            continue

        m = mexp.head(1).to_dict('records')[0]

        ls =  chain[(chain[quote.EXP_DATE] == exp_date) & (m[quote.STRIKE]- chain[quote.STRIKE] > 0) & (m[quote.STRIKE] - chain[quote.STRIKE] <= max_spread)]
        if ls.shape[0] == 0:
            continue  

        for i, l in ls.iterrows():                      
            spread = m[quote.STRIKE] - l[quote.STRIKE]            
            hs =  chain[(chain[quote.EXP_DATE] == exp_date)  & (chain[quote.STRIKE] - m[quote.STRIKE] == spread)]          
            if hs.shape[0] == 0:
                continue
            h = hs.head(1).to_dict('records')[0]     

            df = create_buttrfly_df(strategy, target_low, target_high, l=l, m=m, h=h)              
            if df.shape[0] > 0:
                butterfly_df = pd.concat([butterfly_df, df])

    if butterfly_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (butterfly_df[pscl.OPEN_PRICE].min(), butterfly_df[pscl.OPEN_PRICE].max())
    i = butterfly_df.shape[0]
    butterfly_df = butterfly_df[butterfly_df[pscl.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduce by open price >= %.2f %s' % (i, butterfly_df.shape[0], min_price, open_price_range))

    if math.isnan(min_win_prob) == False:
        win_prob_range = '[%.2f|%.2f]' % (butterfly_df[pscl.WIN_PROB].min(), butterfly_df[pscl.WIN_PROB].max())
        i = butterfly_df.shape[0]
        butterfly_df= butterfly_df[butterfly_df[pscl.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, butterfly_df.shape[0], min_win_prob, win_prob_range))

    if math.isnan(min_pnl) == False:
        pnl_range = '[%.2f|%.2f]' % (butterfly_df[pscl.PNL].min(), butterfly_df[pscl.PNL].max())
        i = butterfly_df.shape[0]
        butterfly_df= butterfly_df[butterfly_df[pscl.PNL] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, butterfly_df.shape[0], min_pnl, pnl_range))

    if credit:
        i = butterfly_df.shape[0]               
        #butterfly_df = butterfly_df[((butterfly_df[pscl.BREAKEVEN_L]/butterfly_df[pscl.TARGET_LOW])<1.05) &  ((butterfly_df[pscl.BREAKEVEN_H]/butterfly_df[pscl.TARGET_HIGH]) > 1.01)]  
        #logger.debug('%d -> %d reduced l/low < 1.05 h/high > 1.01' % (i, butterfly_df.shape[0]))        
        '''
        [ccb All] [55.10%|54|44]	[5142.54|-917.89]	100.00%
            HIT	 [35.85%|19|34]	[6631.37|-920.21]	19.39%
            UNDER	 [75.00%|27|9]	[2322.67|-948.44]	27.55%
            ABOVE	 [88.89%|8|1]	[11123.62|-564.00]	8.16%
        [ccb l/low <1.05 or h/high > 1.01] [65.22%|15|8]	[7406.73|-877.88]	23.47%
            HIT	 [50.00%|4|4]	[2722.75|-1180.25]	4.08%
            UNDER	 [72.73%|8|3]	[2707.50|-579.33]	8.16%
            ABOVE	 [75.00%|3|1]	[26183.33|-564.00]	3.06%        
        '''
    else:
        i = butterfly_df.shape[0]               
        #butterfly_df = butterfly_df[((butterfly_df[pscl.BREAKEVEN_L]/butterfly_df[pscl.TARGET_LOW])<1.25)]
        #logger.debug('%d -> %d reduced l/low < 1.25' % (i, butterfly_df.shape[0]))    
        '''
        [dcb All] [30.00%|9|21]	[815.33|-1314.29]	100.00%
            HIT	 [37.50%|9|15]	[815.33|-1065.60]	30.00%
            UNDER	 [0.00%|0|2]	[nan|-1244.00]	0.00%
            ABOVE	 [0.00%|0|4]	[nan|-2282.00]	0.00%
        ----------------l/low < r ---------------------
        [dcb l/low<1.02] [32.14%|9|19]	[815.33|-1398.95]	93.33%
            HIT	 [40.91%|9|13]	[815.33|-1151.08]	30.00%
            UNDER	 [0.00%|0|2]	[nan|-1244.00]	0.00%
            ABOVE	 [0.00%|0|4]	[nan|-2282.00]	0.00%
        '''        

    return butterfly_df

def pick_put_butterfly(symbol,                          
                    predictlist,
                    spread_list=[],
                    credit=True,
                    max_spread=10,
                    max_strike_ratio=0.25,
                    min_price = np.nan,                             
                    min_pnl=np.nan,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=0):
    
    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    chain = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)
        

    butterfly_df = pd.DataFrame()

    strategy = st.CREDIT_PUT_BUTTERFLY if credit else st.DEBIT_PUT_BUTTERFLY

    for exp_date in exp_date_list:
        
        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        target_price = (predictlist[exp_date][quote.HIGH]+predictlist[exp_date][quote.LOW])/2

        mall = chain[(abs(chain[quote.STRIKE]-target_price) < 2.5)]
        if mall.shape[0] == 0:
            continue    

        mexp = mall[mall[quote.EXP_DATE]==exp_date]
        if mexp.shape[0] == 0:
            continue
        m = mexp.head(1).to_dict('records')[0]        
        ls =  chain[(chain[quote.EXP_DATE] == exp_date) & (m[quote.STRIKE]- chain[quote.STRIKE] > 0) & (m[quote.STRIKE] - chain[quote.STRIKE] <= max_spread)]
        if ls.shape[0] == 0:
            continue  
        for i, l in ls.iterrows():                      
            spread = m[quote.STRIKE] - l[quote.STRIKE]              
            hs =  chain[(chain[quote.EXP_DATE] == exp_date)  & (chain[quote.STRIKE]-m[quote.STRIKE]==spread)]          
            if hs.shape[0] == 0:
                continue
            h = hs.head(1).to_dict('records')[0]                
            df = create_buttrfly_df(strategy, target_low, target_high, l=l, m=m, h=h)  
            if df.shape[0] > 0:
                butterfly_df = pd.concat([butterfly_df, df])

    if butterfly_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (butterfly_df[pscl.OPEN_PRICE].min(), butterfly_df[pscl.OPEN_PRICE].max())
    i = butterfly_df.shape[0]
    butterfly_df = butterfly_df[butterfly_df[pscl.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, butterfly_df.shape[0], min_price, open_price_range))

    if math.isnan(min_win_prob) == False:
        win_prob_range = '[%.2f|%.2f]' % (butterfly_df[pscl.WIN_PROB].min(), butterfly_df[pscl.WIN_PROB].max())
        i = butterfly_df.shape[0]
        butterfly_df= butterfly_df[butterfly_df[pscl.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, butterfly_df.shape[0], min_win_prob, win_prob_range))

    if math.isnan(min_pnl) == False:
        pnl_range = '[%.2f|%.2f]' % (butterfly_df[pscl.PNL].min(), butterfly_df[pscl.PNL].max())
        i = butterfly_df.shape[0]
        butterfly_df= butterfly_df[butterfly_df[pscl.PNL] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, butterfly_df.shape[0], min_pnl, pnl_range))

    if credit:
        i = butterfly_df.shape[0]               
        #butterfly_df = butterfly_df[((butterfly_df[pscl.BREAKEVEN_L]/butterfly_df[pscl.TARGET_LOW])<1.04) &  ((butterfly_df[pscl.BREAKEVEN_H]/butterfly_df[pscl.TARGET_HIGH]) > 1.02)]
        #logger.debug('%d -> %d reduced l/low < 1.04 & h/high > 1.02' % (i, butterfly_df.shape[0]))     
        '''
        [cpb All] [52.48%|53|48]	[1454.72|-985.85]	100.00%
            HIT	 [35.85%|19|34]	[1859.63|-1010.53]	18.81%
            UNDER	 [71.43%|30|12]	[1261.83|-1034.33]	29.70%
            ABOVE	 [66.67%|4|2]	[978.00|-275.50]	3.96%
        [cpb l/low <1.04 or h/high > 1.02] [70.59%|12|5]	[1233.67|-771.80]	16.83%
            HIT	 [57.14%|4|3]	[892.75|-928.67]	3.96%
            UNDER	 [80.00%|8|2]	[1404.12|-536.50]	7.92%
        '''        
    else:
        i = butterfly_df.shape[0]               
        #butterfly_df = butterfly_df[((butterfly_df[pscl.BREAKEVEN_L]/butterfly_df[pscl.TARGET_LOW])<0.99) &  ((butterfly_df[pscl.BREAKEVEN_H]/butterfly_df[pscl.TARGET_HIGH]) > 0.98)]
        #logger.debug('%d -> %d reduced l/low < 0.99 & h/high > 0.98' % (i, butterfly_df.shape[0]))     

        '''
        [dpb All] [44.74%|17|21]	[1483.71|-1053.29]	100.00%
            HIT	 [44.83%|13|16]	[1309.38|-814.75]	34.21%
            UNDER	 [100.00%|4|0]	[2050.25|nan]	10.53%
            ABOVE	 [0.00%|0|5]	[nan|-1816.60]	0.00%
        ---------------l/low < x and h/high > y ----------------------
        [dpb l/low <0.99 and h/high > 0.98] [60.00%|9|6]	[1164.44|-1232.83]	39.47%
            HIT	 [80.00%|8|2]	[1232.50|-60.00]	21.05%
            UNDER	 [100.00%|1|0]	[620.00|nan]	2.63%
            ABOVE	 [0.00%|0|4]	[nan|-1819.25]	0.00%

        '''
    return butterfly_df

def pick_iron_butterfly(symbol,      
                    predictlist,                    
                    spread_list=[],
                    credit=True,
                    max_spread=10,
                    max_strike_ratio=0.25,
                    min_price = np.nan,
                    min_pnl=np.nan,                                
                    min_win_prob=np.nan,
                    max_bid_ask_spread=np.nan,
                    min_open_interest=0):

    logger = logging.getLogger(__name__)   

    exp_date_list = predictlist['exp_date_list']

    put_chain = get_option_chain(symbol, 
                            at.PUT,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)

    call_chain = get_option_chain(symbol, 
                            at.CALL,                         
                            exp_date_list=exp_date_list,
                            max_strike_ratio=max_strike_ratio,
                            max_bid_ask_spread=max_bid_ask_spread,
                            min_open_interest=min_open_interest)


    butterfly_df = pd.DataFrame()

    strategy = st.IRON_BUTTERFLY if credit else st.REVERSE_IRON_BUTTERFLY

    for exp_date in exp_date_list:

        target_low = predictlist[exp_date][quote.LOW]    

        target_high = predictlist[exp_date][quote.HIGH]    

        target_price = (predictlist[exp_date][quote.HIGH]+predictlist[exp_date][quote.LOW])/2

        pmall = put_chain[(abs(put_chain[quote.STRIKE]-target_price) < 2.5)]

        cmall = call_chain[(abs(call_chain[quote.STRIKE]-target_price) < 2.5)]

        if cmall.shape[0] == 0 or pmall.shape[0] == 0:
            continue    

        pmexp = pmall[pmall[quote.EXP_DATE]==exp_date]
        if pmexp.shape[0] == 0:
            continue

        m = pmexp.head(1).to_dict('records')[0]    

        cmexp = cmall[(cmall[quote.EXP_DATE]==exp_date) & (cmall[quote.STRIKE] == m[quote.STRIKE])]
        if cmexp.shape[0] == 0:
            continue

        iron = cmexp.head(1).to_dict('records')[0] 

        ls =  put_chain[(put_chain[quote.EXP_DATE] == exp_date) & (m[quote.STRIKE]- put_chain[quote.STRIKE] > 0) & (m[quote.STRIKE] - put_chain[quote.STRIKE] <= max_spread)]
        if ls.shape[0] == 0:
            continue  

        for i, l in ls.iterrows():               
            spread = m[quote.STRIKE] - l[quote.STRIKE]       
            hs =  call_chain[(call_chain[quote.EXP_DATE] == exp_date)  & (call_chain[quote.STRIKE] - m[quote.STRIKE] == spread)]          
            if hs.shape[0] == 0:
                continue
            h = hs.head(1).to_dict('records')[0] 
            df = create_buttrfly_df(strategy, target_low, target_high, l=l, m=m, h=h, iron=iron)              
            if df.shape[0] > 0:
                butterfly_df = pd.concat([butterfly_df, df])

    if butterfly_df.shape[0] == 0:
        return pd.DataFrame()
    
    open_price_range = '[%.2f|%.2f]' % (butterfly_df[pscl.OPEN_PRICE].min(), butterfly_df[pscl.OPEN_PRICE].max())
    i = butterfly_df.shape[0]
    butterfly_df = butterfly_df[butterfly_df[pscl.OPEN_PRICE] >= min_price]
    logger.debug('%d -> %d reduced by open price >= %.2f %s' % (i, butterfly_df.shape[0], min_price, open_price_range))

    if math.isnan(min_win_prob) == False:
        win_prob_range = '[%.2f|%.2f]' % (butterfly_df[pscl.WIN_PROB].min(), butterfly_df[pscl.WIN_PROB].max())
        i = butterfly_df.shape[0]
        butterfly_df= butterfly_df[butterfly_df[pscl.WIN_PROB] >= min_win_prob]
        logger.debug('%d -> %d reduced by win prob >= %.2f %s' % (i, butterfly_df.shape[0], min_win_prob, win_prob_range))

    if math.isnan(min_pnl) == False:
        pnl_range = '[%.2f|%.2f]' % (butterfly_df[pscl.PNL].min(), butterfly_df[pscl.PNL].max())
        i = butterfly_df.shape[0]
        butterfly_df= butterfly_df[butterfly_df[pscl.PNL] >= min_pnl]
        logger.debug('%d -> %d reduced by pnl >= %.2f %s' % (i, butterfly_df.shape[0], min_pnl, pnl_range))

    if credit:
        i = butterfly_df.shape[0]               
        #butterfly_df = butterfly_df[((butterfly_df[pscl.BREAKEVEN_L]/butterfly_df[pscl.TARGET_LOW])<0.99) &  ((butterfly_df[pscl.BREAKEVEN_H]/butterfly_df[pscl.TARGET_HIGH]) > 0.99)]
        #logger.debug('%d -> %d reduced l/low < 0.99 & h/high > 0.99' % (i, butterfly_df.shape[0]))     

        '''
            [ib All] [60.94%|39|25]	[644.08|-636.60]	100.00%
            HIT	 [70.00%|21|9]	[628.48|-393.00]	32.81%
            UNDER	 [56.25%|18|14]	[662.28|-848.71]	28.12%
            ABOVE	 [0.00%|0|2]	[nan|-248.00]	0.00%
            ---------------l/low < x and h/high > y ---------------------
            [ib l/low <0.99 and h/high > 0.99] [60.71%|17|11]	[697.00|-765.82]	43.75%
                HIT	 [88.89%|8|1]	[716.12|-16.00]	12.50%
                UNDER	 [52.94%|9|8]	[680.00|-989.00]	14.06%
                ABOVE	 [0.00%|0|2]	[nan|-248.00]	0.00%
        '''
    else:
        i = butterfly_df.shape[0]               
        #butterfly_df = butterfly_df[((butterfly_df[pscl.BREAKEVEN_L]/butterfly_df[pscl.TARGET_LOW])<0.98) ]
        #logger.debug('%d -> %d reduced l/low < 0.98' % (i, butterfly_df.shape[0]))                     
    '''
    [rib All] [57.58%|38|28]	[1692.68|-714.46]	100.00%
        HIT	 [50.00%|24|24]	[1277.67|-733.67]	36.36%
        UNDER	 [69.23%|9|4]	[813.33|-599.25]	13.64%
        ABOVE	 [100.00%|5|0]	[5267.60|nan]	7.58%
    ----------------l/low < r ---------------------
    [rib l/low<0.98] [72.73%|8|3]	[2600.62|-1043.33]	16.67%
        HIT	 [87.50%|7|1]	[2807.86|-1288.00]	10.61%
        UNDER	 [0.00%|0|2]	[nan|-921.00]	0.00%
        ABOVE	 [100.00%|1|0]	[1150.00|nan]	1.52%

    '''
    return butterfly_df

def create_single_df(leg, stock_price, target_high, target_low, credit=True):

    dt = {}
    symbol      = leg[quote.SYMBOL]
    today       = datetime.now(timezone(app_settings.TIMEZONE))   
    price       = leg[quote.PRICE]    
    exp_date    = leg[quote.EXP_DATE]
    symbol      = leg[quote.SYMBOL]
    otype       = leg[quote.OTYPE]
    strike      = leg[quote.STRIKE]    
    margin      = stock_price if credit else 0.0

    if otype == at.CALL:
        strategy = st.COVERED_CALL if credit else st.LONG_CALL
        dt[pscl.STRATEGY] = [strategy]         
        if credit:
            max_profit = price
            max_loss = stock_price-price            
            #max_loss = strike-target_low-price
            breakeven_h =  strike-price
            breakeven_l =  np.nan
        else:
            max_profit = target_high-strike-price
            max_loss = price
            breakeven_l =  strike+price
            breakeven_h =  np.nan
    else:
        strategy = st.SHORT_PUT if credit else st.LONG_PUT
        dt[pscl.STRATEGY] = [strategy]        
        pnl = stock_price if credit else np.nan
        if credit:
            max_profit = price
            max_loss = strike-price                
            #max_loss = target_high-strike-price            
            breakeven_l =  strike-price
            breakeven_h =  np.nan
        else:
            max_profit = strike-target_low-price
            max_loss = price            
            breakeven_h =  strike-price
            breakeven_l =  np.nan

    win_prob = calc_win_prob(symbol, exp_date, strategy, breakeven_l, breakeven_h)            

    if max_profit <= 0 or max_loss <= 0:
        return pd.DataFrame()
    
    pnl = max_profit / max_loss

    dt[pscl.SYMBOL]            = [symbol]
    dt[pscl.EXP_DATE]          = [exp_date]
    dt[pscl.OPEN_PRICE]        = [price]
    dt[pscl.LAST_PRICE]        = [price]    
    dt[pscl.PNL]               = [pnl]
    dt[pscl.WIN_PROB]          = [win_prob]
    dt[pscl.MAX_LOSS]          = [max_loss]
    dt[pscl.MAX_PROFIT]        = [max_profit]
    dt[pscl.MARGIN]            = [margin]
    dt[pscl.BREAKEVEN_H]       = [breakeven_h]
    dt[pscl.BREAKEVEN_L]       = [breakeven_l]
    dt[pscl.TRADE_DATE]        = [today]
    dt[pscl.TRADE_STOCK_PRICE] = [stock_price]
    dt[pscl.SPREAD]            = [np.nan]

    dt[pscl.TARGET_HIGH]       = [target_high]
    dt[pscl.TARGET_LOW]        = [target_low]       

    leg[pcl.SCALE]                 = 1
    leg[pcl.OPEN_ACTION] = at.SELL_TO_OPEN if credit else at.BUY_TO_OPEN    

    dt[pscl.LEGS] = [[leg]]

    df = pd.DataFrame.from_dict(dt)

    return df

def create_spread_df(target_low, target_high, sleg, lleg, otype, credit=True):

    logger = logging.getLogger(__name__)   

    dt = {}

    if (credit) & (sleg[quote.PRICE] <= lleg[quote.PRICE]):
        return pd.DataFrame()
    
    if ~(credit) & (sleg[quote.PRICE] >= lleg[quote.PRICE]):
        return pd.DataFrame()

    symbol   = sleg[quote.SYMBOL]
    exp_date = sleg[quote.EXP_DATE]
    spread = abs(sleg[quote.STRIKE]-lleg[quote.STRIKE])

    price =  abs(sleg[quote.PRICE]-lleg[quote.PRICE])
    max_profit = price if credit else spread-price
    max_loss = (spread - price) if credit else price
    if max_loss == 0:
        logger.debug('noway')
        pass

    today = datetime.now(timezone(app_settings.TIMEZONE))
    stock_price = get_price(symbol)

    if max_profit <= 0 or max_loss <= 0:
        return pd.DataFrame()
    
    pnl = max_profit / max_loss
    margin = spread if credit else 0.0

    if otype == at.CALL:
        strategy = st.CREDIT_CALL_SPREAD if credit else st.DEBIT_CALL_SPREAD        
        dt[pscl.STRATEGY] = [strategy]      
        if credit:
            breakeven_h =sleg[quote.STRIKE]+price
            breakeven_l = np.nan               
        else:
            breakeven_l =lleg[quote.STRIKE]+price 
            breakeven_h = np.nan           
    else:
        strategy = st.CREDIT_PUT_SPREAD if credit else st.DEBIT_PUT_SPREAD
        dt[pscl.STRATEGY] = [strategy]        
        if credit:
            breakeven_l =sleg[quote.STRIKE]-price
            breakeven_h = np.nan        
        else:
            breakeven_h =lleg[quote.STRIKE]-price 
            breakeven_l = np.nan

    win_prob = calc_win_prob(symbol, exp_date, strategy, breakeven_l, breakeven_h)              

    dt[pscl.SYMBOL]            = [symbol]
    dt[pscl.EXP_DATE]          = [exp_date]
    dt[pscl.SPREAD]            = [spread]         
    dt[pscl.LAST_PRICE]        = [price]
    dt[pscl.OPEN_PRICE]        = [price]   
    dt[pscl.MAX_LOSS]          = [max_loss]
    dt[pscl.MAX_PROFIT]        = [max_profit]
    dt[pscl.MARGIN]            = [margin]
    dt[pscl.PNL]               = [pnl]
    dt[pscl.BREAKEVEN_H]       = [breakeven_h]
    dt[pscl.BREAKEVEN_L]       = [breakeven_l]
    dt[pscl.WIN_PROB]          = [win_prob] 
    dt[pscl.TRADE_DATE]        = [today] 
    dt[pscl.TRADE_STOCK_PRICE] = [stock_price]
    dt[pscl.TARGET_HIGH]       = [target_high]
    dt[pscl.TARGET_LOW]        = [target_low]    

    sleg[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
    lleg[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
    sleg[pcl.SCALE] = 1
    lleg[pcl.SCALE] = 1
    sleg[pcl.SYMBOL] = lleg[pcl.SYMBOL] = symbol
    sleg[pcl.EXP_DATE] = lleg[pcl.EXP_DATE] = exp_date
 

    dt[pscl.LEGS] = [[sleg, lleg]]

    df = pd.DataFrame.from_dict(dt)
    
    return df

def create_buttrfly_df(strategy, target_low, target_high, l={}, m={}, h={}, iron={}):
  
    logger = logging.getLogger(__name__)   

    dt = {}

    symbol          = m[quote.SYMBOL]
    spread          = m[quote.STRIKE]-l[quote.STRIKE]
    exp_date        = m[quote.EXP_DATE]
    days_to_expire  = m[quote.DAYS_TO_EXPIRE]  
    stock_price     = get_price(symbol)
    today           = datetime.now(timezone(app_settings.TIMEZONE))

    m[pcl.SYMBOL]   = l[pcl.SYMBOL]   = h[pcl.SYMBOL] = symbol
    m[pcl.EXP_DATE] = l[pcl.EXP_DATE] = h[pcl.EXP_DATE] = exp_date

    if strategy == st.DEBIT_CALL_BUTTERFLY:
     
        price       = (2 * m[quote.PRICE]) - l[quote.PRICE] - h[quote.PRICE]   
        if price >= 0: # bad quote date?
            return pd.DataFrame()
        
        price = abs(price)

        margin = 0.0
        max_loss = price
        max_profit = spread-price
        
        breakeven_l = m[quote.STRIKE] - spread-price    
        breakeven_h = m[quote.STRIKE] + spread-price 

        l[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        m[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        h[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        l[pcl.SCALE] = 1
        m[pcl.SCALE] = 2
        h[pcl.SCALE] = 1
        legs =  [l, m, h]
    elif strategy == st.CREDIT_CALL_BUTTERFLY:
 
        price       = l[quote.PRICE] + h[quote.PRICE] - (2 * m[quote.PRICE])        
        if price <= 0: # bad quote date?
            return pd.DataFrame()
                
        max_profit = price
        max_loss = spread-price       
        margin = spread

        breakeven_l = m[quote.STRIKE] - spread-price    
        breakeven_h = m[quote.STRIKE] + spread-price 
        
        l[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        m[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        h[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        l[pcl.SCALE] = 1
        m[pcl.SCALE] = 2
        h[pcl.SCALE] = 1

        legs = [l, m, h]
    elif strategy == st.CREDIT_PUT_BUTTERFLY:         
  
        price       = l[quote.PRICE] + h[quote.PRICE] - (2 * m[quote.PRICE])        
        if price <= 0: # bad quote date?
            return pd.DataFrame()
        
        max_profit = price
        max_loss = spread-price       
        margin = spread
        breakeven_l = m[quote.STRIKE] - spread-price    
        breakeven_h = m[quote.STRIKE] + spread-price 
                  
        l[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        m[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        h[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        l[pcl.SCALE] = 1
        m[pcl.SCALE] = 2
        h[pcl.SCALE] = 1        
        legs =[l, m, h]
    elif strategy == st.DEBIT_PUT_BUTTERFLY: 

        price       = (2 * m[quote.PRICE]) - l[quote.PRICE] - h[quote.PRICE]
        if price >= 0: # bad quote date?
            return pd.DataFrame()

        price = abs(price)

        max_loss = price
        max_profit = spread-price       
        margin = 0.0
        breakeven_l = m[quote.STRIKE] - spread-price    
        breakeven_h = m[quote.STRIKE] + spread-price   

        l[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        m[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        h[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        l[pcl.SCALE] = 1
        m[pcl.SCALE] = 2
        h[pcl.SCALE] = 1
        legs = [l,m,h]
    elif strategy == st.REVERSE_IRON_BUTTERFLY:

        price       = l[quote.PRICE] + h[quote.PRICE] - m[quote.PRICE] - iron[quote.PRICE]      
        if price >= 0:
            return pd.DataFrame()  
        
        price = abs(price)
        
        max_loss = price
        max_profit = spread-price       
        margin = 0.0
        breakeven_l = m[quote.STRIKE] - spread-price    
        breakeven_h = m[quote.STRIKE] + spread-price  
        
        l[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        m[pcl.OPEN_ACTION] = at.BUY_TO_OPEN        
        iron[pcl.OPEN_ACTION] =at.BUY_TO_OPEN
        h[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        l[pcl.SCALE] = 1
        m[pcl.SCALE] = 1
        iron[pcl.SCALE] = 1        
        h[pcl.SCALE] = 1

        legs = [l, m, iron, h]
    elif strategy  == st.IRON_BUTTERFLY:
        credit  = True
        price   = m[quote.PRICE] + iron[quote.PRICE] - l[quote.PRICE] - h[quote.PRICE] 
        if price <= 0:
            return pd.DataFrame()  

        max_loss = spread-price
        max_profit = price       
        margin = spread
        breakeven_l = m[quote.STRIKE] - spread-price    
        breakeven_h = m[quote.STRIKE] + spread-price 

        l[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        m[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        iron[pcl.OPEN_ACTION] = at.SELL_TO_OPEN
        h[pcl.OPEN_ACTION] = at.BUY_TO_OPEN
        
        l[pcl.SCALE] = 1
        m[pcl.SCALE] = 1
        iron[pcl.SCALE] = 1        
        h[pcl.SCALE] = 1

        legs = [l, m, iron, h]
    else:
        logger.error("Unknown strategy %s" % strategy)
        return pd.DataFrame()

    win_prob = calc_win_prob(symbol, exp_date,  strategy, breakeven_l, breakeven_h)        

    if max_loss <= 0 or max_profit <= 0:
        return pd.DataFrame()
    
    pnl = np.nan if max_loss == 0 else max_profit / max_loss
                                   
    dt[pscl.SYMBOL]            = [symbol]
    dt[pscl.STRATEGY]          = [strategy]
    dt[pscl.SPREAD]            = [spread]
    dt[pscl.EXP_DATE]          = [exp_date]
    dt[pscl.LAST_PRICE]        = [price]
    dt[pscl.OPEN_PRICE]        = [price]   

    dt[pscl.MAX_PROFIT]        = [max_profit]
    dt[pscl.MAX_LOSS]          = [max_loss]
    dt[pscl.MARGIN]            = [margin]    
    dt[pscl.PNL]               = [pnl]
    dt[pscl.BREAKEVEN_H]       = [breakeven_h]
    dt[pscl.BREAKEVEN_L]       = [breakeven_l]

    dt[pscl.WIN_PROB]          = [win_prob] 

    dt[pscl.TRADE_DATE]        = [today] 
    dt[pscl.TRADE_STOCK_PRICE] = [stock_price]
    dt[pscl.TARGET_HIGH]       = [target_high]
    dt[pscl.TARGET_LOW]        = [target_low]    

    dt[pscl.LEGS] = [legs]
    df = pd.DataFrame.from_dict(dt)
    return df

def create_iron_condor_df(strategy, target_low, target_high, pl=None, ph=None, cl=None, ch=None):
    
    logger = logging.getLogger(__name__)   

    dt = {}

    symbol = pl[quote.SYMBOL]

    if strategy not in [st.CREDIT_IRON_CONDOR, st.DEBIT_IRON_CONDOR]:
        logger.error('Unsupported strategy %s' % strategy)
        return pd.DataFrame()
    
    #if abs(ph[quote.STRIKE]-pl[quote.STRIKE]) != abs(ch[quote.STRIKE]-cl[quote.STRIKE]):
    #    logger.error('%s Put spread %.2f Call spread %.2f not the same' % (symbol, abs(ph[quote.STRIKE]-pl[quote.STRIKE]), abs(ch[quote.STRIKE]-cl[quote.STRIKE])))
    #    return pd.DataFrame()

    credit = True if strategy == st.CREDIT_IRON_CONDOR else False

    if (ph[quote.PRICE] <= pl[quote.PRICE]) or (cl[quote.PRICE] <= ch[quote.PRICE]):
        return pd.DataFrame()
    
    dt[pscl.STRATEGY] = [strategy]
    dt[pscl.TRADE_DATE] = datetime.now(timezone(app_settings.TIMEZONE))
    dt[pscl.TRADE_STOCK_PRICE] = get_price(symbol)

    spread = abs(ph[quote.STRIKE]-pl[quote.STRIKE])
    price = abs(ph[quote.PRICE]-pl[quote.PRICE]) + abs(ch[quote.PRICE]-cl[quote.PRICE])
    max_loss = spread-price if credit else price 
    max_profit = price if credit else spread-price 

    if max_profit <= 0 or max_loss <= 0:
        return pd.DataFrame()
    
    margin = spread if credit else 0.0
    exp_date   = ph[quote.EXP_DATE]
    breakeven_l = ph[quote.STRIKE] - price if credit else ph[quote.STRIKE] - price
    breakeven_h = cl[quote.STRIKE] + price if credit else ch[quote.STRIKE] - price
    days_to_expire = ph[quote.DAYS_TO_EXPIRE]
    dt[pscl.EXP_DATE]    = [exp_date]
    dt[pscl.SYMBOL]      = [symbol]
    dt[pscl.SPREAD]      = [spread]
    dt[pscl.OPEN_PRICE]  = [price]    
    dt[pscl.LAST_PRICE]  = [price]
    dt[pscl.EXP_DATE]    = [exp_date]
    dt[pscl.MAX_PROFIT]  = [max_profit]
    dt[pscl.MAX_LOSS]    = [max_loss]
    dt[pscl.MARGIN]      = [margin]    
    dt[pscl.PNL]         = [np.nan] if max_loss == 0 else [max_profit / max_loss]
    dt[pscl.BREAKEVEN_H] = [breakeven_h]
    dt[pscl.BREAKEVEN_L] = [breakeven_l]
    dt[pscl.TARGET_HIGH] = [target_high]
    dt[pscl.TARGET_LOW]  = [target_low]       

    win_prob = calc_win_prob(symbol, exp_date, strategy, breakeven_l, breakeven_h)
    
    dt[pscl.WIN_PROB]  = [win_prob] 

    ph[pcl.SYMBOL] = pl[pcl.SYMBOL] = ch[pcl.SYMBOL] = cl[pcl.SYMBOL] = symbol
    ph[pcl.EXP_DATE] = pl[pcl.EXP_DATE] = ch[pcl.EXP_DATE] = cl[pcl.EXP_DATE] = exp_date
    ph[pcl.SCALE] = pl[pcl.SCALE] = ch[pcl.SCALE] = cl[pcl.SCALE] = 1

    ph[pcl.OPEN_ACTION] = at.SELL_TO_OPEN if credit else at.BUY_TO_OPEN
    pl[pcl.OPEN_ACTION] = at.BUY_TO_OPEN if credit else at.SELL_TO_OPEN
    ch[pcl.OPEN_ACTION] = at.BUY_TO_OPEN if credit else at.SELL_TO_OPEN
    cl[pcl.OPEN_ACTION] = at.SELL_TO_OPEN if credit else at.BUY_TO_OPEN


    dt[pscl.LEGS] = [[ph, pl, ch, cl]]

    df = pd.DataFrame.from_dict(dt)

    return df

def get_price(symbol):
    df = get_price_history(symbol, period='1d')
    if df.shape[0] == 0:
        return np.nan
    return df['Close'][0]

if __name__ == '__main__':

    #import sys
    import numpy as np

    #sys.path.append(r'\Users\jimhu\option_trader\src')
    from option_trader.consts import asset as at
    from option_trader.utils.data_getter import get_option_chain
    from option_trader.utils.data_getter import get_price_history
    from option_trader.utils.data_getter import pick_call_butterfly
    from option_trader.utils.predictor import predict_price_range

    import warnings
    warnings.filterwarnings("ignore")

    import logging
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("yfinance").setLevel(logging.WARNING)    
    
    from option_trader.settings.log_config import LOGGING
    #LOGGING['loggers']['']['level'] = 'DEBUG'
    #logging.config.dictConfig(LOGGING)

    symbol = 'BLDR'

    print(get_price(symbol))

    exit(0)

    predictlist = predict_price_range(symbol)

    df =  pick_vertical_put_spreads(  symbol,  
                                        predictlist,                      
                                        credit=True,
                                        max_spread = 10,
                                        max_strike_ratio=0.25,
                                        min_win_prob=50,
                                        min_pnl=40)
    print(df)

    exit(0)

    print(get_option_exp_date(symbol))

    exit(0)

    current_price = get_price(symbol)

    iv, delta = get_option_leg_IV_delta(symbol, datetime.strptime('2023-06-09','%Y-%m-%d').date(), datetime.strptime('2023-06-16','%Y-%m-%d').date(), current_price, at.CALL)
    print(iv)
    print(delta)
    #print(get_option_leg_IV(symbol, '2023-06-16', 300, at.PUT))

    exit(0)

    current_price =get_price(symbol)

    target_upper_price =  current_price + 5

    target_lower_price = current_price - 5


    cic = pick_iron_condor(symbol,                          
                            target_upper_price,
                            target_lower_price,
                            credit=False,
                            min_price= 0,
                            max_spread = 10,
                            exp_date_list=[],
                            spread_list=[],
                            min_pnl=0.0,
                            min_win_prob=50,
                            min_annualized_return=0,
                            max_bid_ask_spread=10,
                            max_days_to_expire=90, 
                            min_open_interest=100)

    def dump_chain(chain):
        print('----------')    
        print(chain[[quote.DAYS_TO_EXPIRE, quote.SPREAD, quote.PRICE, quote.MAX_PROFIT, quote.MARGIN, quote.MAX_LOSS, quote.PNL, quote.WIN_PROB, quote.BREAKEVEN_L, quote.BREAKEVEN_H, quote.ANNUALIZED_RETURN, quote.P1_ST, quote.P1_SK, quote.P1_LK, quote.P2_ST, quote.P2_SK, quote.P2_LK]])


    if cic.shape[0] > 0:
        dump_chain(cic)