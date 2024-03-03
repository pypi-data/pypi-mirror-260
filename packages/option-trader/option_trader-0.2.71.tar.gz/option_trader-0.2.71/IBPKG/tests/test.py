import sys

#sys.path.append(r'C:\\TWS API\source\\pythonclient\\')
sys.path.append(r'C:\\Users\\jimhu\\option_trader\src\\IBPKG')

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.utils import floatMaxString, decimalMaxString

from threading import Timer

class TestApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString, advancedOrderRejectJson):
        super().error(reqId, errorCode, errorString, advancedOrderRejectJson)
        print("Error: ", reqId, " ", errorCode, " ", errorString, " ", advancedOrderRejectJson )

    def nextValidId(self, orderId):
        super().nextValidId(orderId)
        self.start(orderId)

    def updatePortfolio(self, contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName):
        super().updatePortfolio(contract, position, marketPrice, marketValue,averageCost, unrealizedPNL, realizedPNL, accountName)
        print("UpdatePortfolio.", "Symbol:", contract.symbol, "SecType:", contract.secType, "Exchange:", contract.exchange,
              "Position:", position, "MarketPrice:", marketPrice, "MarketValue:", marketValue, "AverageCost:", averageCost,
              "UnrealizedPNL:", unrealizedPNL, "RealizedPNL:", realizedPNL, "AccountName:", accountName)

    def updateAccountValue(self, key, val, currency, accountName):
        super().updateAccountValue(key, val, currency, accountName)
        print("UpdateAccountValue. Key:", key, "Value:", val, "Currency:", currency, "AccountName:", accountName)

    def updateAccountTime(self, timeStamp):
        super().updateAccountTime(timeStamp)
        print("UpdateAccountTime. Time:", timeStamp)

    def accountDownloadEnd(self, accountName):
        super().accountDownloadEnd(accountName)
        print("AccountDownloadEnd. Account:", accountName)

    def tickString(self, reqId, tickType, value):
        super().tickString(reqId, tickType, value)
        print("TickString. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    def tickSPrice(self, reqId, tickType, value):
        super().tickPrice(reqId, tickType, value)
        print("TickPrice. TickerId:", reqId, "Type:", TickTypeEnum.toStr(tickType), "Value:", value)

    def tickPrice(self, reqId, tickType, price, attrib):
        super().tickPrice(reqId, tickType, price, attrib)
        print("TickPrice. TickerId:", reqId, "tickType:", TickTypeEnum.toStr(tickType),"Price:", floatMaxString(price), "CanAutoExecute:", attrib.canAutoExecute,"PastLimit:", attrib.pastLimit, end=' ')
        if tickType == TickTypeEnum.BID or tickType == TickTypeEnum.ASK:
            print("PreOpen:", attrib.preOpen)
        else:
            print()

    def tickSize(self, reqId, tickType, size):
        super().tickSize(reqId, tickType, size)
        print("TickSize. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Size: ", decimalMaxString(size))            

    def tickGeneric(self, reqId, tickType, value):
        super().tickGeneric(reqId, tickType, value)
        print("TickGeneric. TickerId:", reqId, "TickType:", TickTypeEnum.toStr(tickType), "Value:", floatMaxString(value))

    def marketDataType(self, reqId, marketDataType):
        super().marketDataType(reqId, marketDataType)
        print("marketDataType. ReqId:", reqId, "Type:", marketDataType)

    def managedAccounts(self, accountsList):
        super().managedAccounts(accountsList)
        print(accountsList)

    def tickSnapshotEnd(self, reqId):
        super().tickSnapshotEnd(reqId)
        print("tickSnapshotEnd. ReqId:", reqId)

    """ market data call back for Exchange for Physical
    tickerId -      The request's identifier.
    tickType -      The type of tick being received.
    basisPoints -   Annualized basis points, which is representative of
        the financing rate that can be directly compared to broker rates.
    formattedBasisPoints -  Annualized basis points as a formatted string
        that depicts them in percentage form.
    impliedFuture - The implied Futures price.
    holdDays -  The number of hold days until the lastTradeDate of the EFP.
    futureLastTradeDate -   The expiration date of the single stock future.
    dividendImpact - The dividend impact upon the annualized basis points
        interest rate.
    dividendsToLastTradeDate - The dividends expected until the expiration
        of the single stock future."""
        
    def tickEFP(self,reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate):
        super().tickEFP(reqId,tickType,basisPoints,formattedBasisPoints,totalDividends,holdDays,
                futureLastTradeDate,dividendImpact,dividendsToLastTradeDate)
        
        print("tickEFP. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "basePosints:", floatMaxString(basisPoints),
              "formattedBasisPoints:", formattedBasisPoints,
              "totalDividends:", totalDividends,
              "holdDays:", holdDays,
              "futureLastTradeDate:", futureLastTradeDate,
              "dividendImpact:", dividendImpact,
              "dividendsToLastTradeDate:",dividendsToLastTradeDate)
    
    def tickOptionComputation(self,reqId,tickType,tickAttrib,impliedVol,delta,optPrice,pvDividend,gamma,vega,theta,undPrice):
        """This function is called when the market in an option or its
        underlier moves. TWS's option model volatilities, prices, and
        deltas, along with the present value of dividends expected on that
        options underlier are received."""

        print("tickOptionComputation. TickerId:", reqId, 
              "TickType:", TickTypeEnum.toStr(tickType), 
              "tickAttrib:", tickAttrib,
              "impliedVol:", impliedVol,
              "delta:", delta,
              "optPrice:", optPrice,
              "pvDividend:", pvDividend,
              "gamma:", gamma,
              "vega:", vega,
              "theta:",  theta,
              "undPrice:", undPrice)              
    
    def start(self, reqId):
        # Account number can be omitted when using reqAccountUpdates with single account structure
        #self.reqAccountUpdates(True, "U11921459")
        contract = Contract()
        contract.symbol = 'MSFT'
        contract.secType = 'OPT'
        contract.exchange = 'SMART'
        contract.currency = 'USD'
        contract.lastTradeDateOrContractMonth = '20231222'
        contract.strike = 370
        contract.right = 'C'
        contract.multiplier = '100'          
        #self.qualifyContracts(contract) 
        self.reqMarketDataType(3)
        self.reqMktData(reqId, contract, '', False, False, [])

    def stop(self):
        self.reqAccountUpdates(False, "U11921459")
        self.done = True
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", 4002, 0)

    Timer(10, app.stop).start()
    app.run()

if __name__ == "__main__":
    main()