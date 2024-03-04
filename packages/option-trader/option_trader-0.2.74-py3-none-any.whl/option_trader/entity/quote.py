SYMBOL              ='symbol'
EXP_DATE            ='exp_date'
OTYPE               ='otype'
OPEN_ACTION         ='open_action'
OPEN                ='open'
HIGH                ='high'
LOW                 ='low'
CLOSE               ='close'
BID_SIZE            ='bidSize'
ASK_SIZE            ='askSize'
LAST_SIZE           ='lastSize'
VOLUME              ='volume'

EXP_DATE            ='exp_date'
STRIKE              ='strike'
PRICE               ='price'
LAST_PRICE          ='lastPrice'
BID                 ='bid'
ASK                 ='ask'
VOLUME              ='volume'
OPEN_INTEREST       ='openInterest'
IMPLIED_VOLATILITY  ='impliedVolatility'

DELTA               ='delta'
GAMMA               ='gamma'
VEGA                ='vega'
THETA               ='theta'
SIGMA               ='sigma'

DAYS_TO_EXPIRE      ='days to expire'
IN_MONEY            = 'in money'
BID_ASK_SPREAD      ='bid ask spread'
STOCK_PRICE         ='stock_price'
#BREAKEVEN_LONG      = 'breakeven_long'
#BREAKEVEN_SHORT     = 'breakeven_short'
#WIN_PROB_LONG       = 'win_prob_long'
#WIN_PROB_SHORT      = 'win_prob_short'
BREAKEVEN           = 'breakeven'
WIN_PROB            = 'win_prob'

import numpy as np

option_chain_rec = {SYMBOL:[''], EXP_DATE:[''],STRIKE:[np.nan],OTYPE:[''],
                    LAST_PRICE:[np.nan], LAST_SIZE:[np.nan],
                    BID:[np.nan], BID_SIZE:[np.nan],
                    ASK:[np.nan], ASK_SIZE:[np.nan],
                    VOLUME:[np.nan], OPEN_INTEREST:[np.nan],
                    OPEN:[np.nan], HIGH:[np.nan],LOW:[np.nan], CLOSE:[np.nan],
                    IMPLIED_VOLATILITY:[np.nan], 
                    DELTA:[np.nan], 
                    GAMMA:[np.nan],
                    VEGA:[np.nan], 
                    THETA:[np.nan]}
