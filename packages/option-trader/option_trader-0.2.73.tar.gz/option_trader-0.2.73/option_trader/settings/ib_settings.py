LocalHostIP =  '127.0.0.1'
DockerHostIP = 'host.docker.internal'

SLEEP_TIME=60

class IBConfig:
    marketDataType = 3 #https://interactivebrokers.github.io/tws-api/market_data_type.html

    class TWS_live:
        port = 7496 
        clientId = 8001

    class TWS_paper:
        port =7497 
        clientId = 8002

    class Gateway_live:
        port =4001 
        clientId = 9001

    class Gateway_paper:
        port =4002 
        clientId = 9002
