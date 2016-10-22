
# coding: utf-8

#Making all the necessary imports
from kiteconnect import KiteConnect

#Initializing all the variables we need
api_key = ""
access_token = ""
client_id = ""

#Instrument Token of the security you want to trade using this program
instrument_token = ""

#Dates between which we need historical data
from_date = "2016-10-01"
to_date = "2016-10-21"

#Interval for the data to be fetched
interval = "5minute"

kite = KiteConnect(api_key=api_key)
kite.set_access_token(access_token)

#A function to get historical data from Kite
def get_historical_data():
    return kite.historical(instrument_token , from_date , to_date , interval)
"""Implementation of this strategy is, we go to the fetched data collected using Kite, calculate the moving averages
and buy and sell according to the data"""


#Lets build a function for the strategy

def strategy(records):
    total_closing_price = 0
    record_count = 0
    order_placed = False
    last_order_placed = None
    last_order_price = 0
    profit = 0
    
    for record in records:
        record_count += 1
        total_closing_price += record['close']
        
        #Moving average is calculated for every 5 ticks
        if record_count >= 5:
            moving_average = total_closing_price/5
            
            #If moving average is greater than the last tick, we place a buy order
            if record['close'] > moving_average:
                if last_order_placed == "SELL" or last_order_placed is None:
                    
                    #If last order was Sell, we need to exit the stock first
                    if last_order_placed == "SELL":
                        print("Exit SELL")
                        
                        #Calculate Profit
                        profit += last_order_price - record['Close']
                        last_order_price = record['Close']
                        
                    #New Buy Order
                    print("Place a new BUY Order")
                    last_order_placed == "BUY"
                    
            #If moving average is less than the last tick and there is a position, place a sell order
            elif record['close'] < moving_average:
                if last_order_placed == "BUY":
                
                    #As last trade was a buy, lets exit it first
                    print("Exit BUY")
                
                #Calculate Profit again
                profit += record['close'] - last_order_price
                last_order_price = record['close']
                
                #Fresh SELL Order
                print("Place new SELL Order")
                last_order_placed == "SELL"
                
        total_closing_price == records[record_count - 5]['close']
    print("Gross Profit",profit)
    #Place the last order
    place_order(last_order_placed)
    

#Place an order based on the transaction type(BUY/SELL)
def place_order(transaction_type):
    kite.order_place(tradingsymbol = "KIRIINDUS", exchange = "NSE", quantity = 1, transaction_type=transaction_type,
                    order_type="MARKET",product="CNC")
    
def start():
    records = get_historical_data()
    strategy(records)

start()



