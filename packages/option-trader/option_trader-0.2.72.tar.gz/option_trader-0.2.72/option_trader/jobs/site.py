import sys

sys.path.append(r'/Users/jimhu/option_trader/src')

from option_trader.jobs import core
from option_trader.admin.site import site
from option_trader.admin.user import user
from option_trader.admin.account import account

from option_trader.consts import strategy 
from option_trader.entity.top_pick import top_pick_mgr

import logging

from option_trader.utils.data_getter import afterHours


DEFAULT_SITE_STRATEGY = [strategy.CREDIT_PUT_SPREAD, strategy.CREDIT_IRON_CONDOR]


class site_refresh_top_pick_job():
    def __init__(self, site_name):     
        self.site_name = site_name
        self.logger = logging.getLogger(__name__)        
        return
    
    def execute(self):

        if afterHours():
            self.logger.info('No top pick refresh, After hours')
            return
        
        with site(self.site_name) as mysite:
            top_pick_mgr(mysite).refresh_top_picks(mysite.get_monitor_list())                  
            
        return
    
class site_refresh_monitorlist_job():
    def __init__(self, site_name):     
        self.site_name = site_name
        self.logger = logging.getLogger(__name__)        
        return
    
    def execute(self):

        if afterHours():
            self.logger.info('No monitor list refresh, After hours')
            return
                
        with site(self.site_name) as mysite:
            mysite.refresh_site_monitor_list()     
            mysite.publish_watchlist_report()                 
        return
    
class site_user_account_summary_report_job():
    def __init__(self, site_name):     
        self.site_name = site_name
        self.logger = logging.getLogger(__name__)        
        return
    
    def execute(self):
                
        with site(self.site_name) as this_site:
            user_list = this_site.get_user_list()
            for user_name in user_list:
                with user(site=this_site, user_name=user_name) as this_user:
                    this_user.send_account_status_report()

                
        return
        
if __name__ == '__main__':
    
    from logging.handlers import RotatingFileHandler
    
    from option_trader.settings import app_settings    

    FORMAT = '%(asctime)s-%(levelname)s (%(message)s) %(filename)s-%(lineno)s-%(funcName)s'
        
    ch = logging.StreamHandler()    
    #ch.setFormatter(formatter)

    import os

    if os.path.exists(app_settings.LOG_ROOT_DIR) == False:        
        os.mkdir(app_settings.LOG_ROOT_DIR)

    import datetime    
    daily_log_path = app_settings.LOG_ROOT_DIR+'\\my_log-'+datetime.date.today().strftime("%Y-%m-%d")+'.log'
    fh = RotatingFileHandler(daily_log_path)
    #fh.setFormatter(formatter)

    logging.basicConfig(
                level=logging.INFO,
                format=FORMAT,
                handlers=[ch, fh]
            )

    logger = logging.getLogger(__name__)

    # Filter paramiko.transport debug and info from basic logging configuration
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARN)

    logging.getLogger('yfinance').setLevel(logging.WARN)

    logger.debug('processing single')


    t = site_refresh_monitorlist_job('mysite')

    t.execute()

    t = site_user_account_summary_report_job('mysite')

    t.execute()    