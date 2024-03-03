
# site.db
site_profile = "site_name TEXT NOT NULL PRIMARY KEY, region TEXT, default_strategy_list TEXT, default_watchlist TEXT, default_notification_token TEXT"

site_monitor_db = "symbol TEXT NOT NULL PRIMARY KEY, last_price REAL, support REAL, resistence REAL,\
    rating REAL, trend TEXT, slope REAL, bb_pos TEXT, bb_link TEXT, rsi TEXT, rsi_link TEXT,\
    macd TEXT, macd_link TEXT, mfi TEXT, mfi_link TEXT, earning TEXT, day_range_pos REAL,\
    fifty_weeks_range_pos REAL, volume_range_pos REAL, forward_PE REAL, HV REAL,\
    IV1 REAL, delta1 REAL,IV2 REAL, delta2 REAL,IV3 REAL, delta3 REAL,IV4 REAL, delta4 REAL,\
    quote_time TEXT, last_update_time TEXT"

user_list = "user_name TEXT NOT NULL PRIMARY KEY, db_path TEXT NOT NULL"

# user.db
user_profile = "name TEXT NOT NULL PRIMARY KEY, email TEXT, default_strategy_list TEXT, default_watchlist TEXT, notification_token TEXT,  billing TEXT, brokerage TEXT"

#watchlist   =  "name TEXT NOT NULL PRIMARY KEY, symbol_list TEXT"

account_list = "account_name TEXT NOT NULL PRIMARY KEY, db_path TEXT NOT NULL"