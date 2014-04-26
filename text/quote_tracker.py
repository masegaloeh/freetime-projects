#!/usr/bin/env python3
import argparse
import sys
import time
import urllib.request

from xml.etree.ElementTree import parse,fromstring

def check_negative(value):
    errMsg = "Interval {} is an invalid positive int value".format(value)
    try:
        retValue = int(value)
    except:
        raise argparse.ArgumentTypeError(errMsg)

    if retValue < 0:
        raise argparse.ArgumentTypeError(errMsg)

    return retValue

def getStockValue(symbol):
    url = "http://dev.markitondemand.com/Api/v2/Quote/xml?symbol={}".format(symbol)
    headers = { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
    try:
        req = urllib.request.Request(url, None, headers)
        data = urllib.request.urlopen(req)
        xmlRoot = fromstring(data.read())
            

        if xmlRoot.tag != "StockQuote":
            print("Company {} not found".format(symbol))
            return None

        xmlDict = {child.tag:child.text for child in xmlRoot}

        if xmlDict.get('Status') is None:
            print("Corrupted Data")
            return None
        elif xmlDict.get('Status') != 'SUCCESS':
            print("Corrupted Data")
            return None
        
        if xmlDict.get('LastPrice') is None or xmlDict.get('Name') is None:
            print("Corrupted Data")
            return None
        else:
            return [xmlDict.get('Name'), float(xmlDict.get('LastPrice'))]
    except:
        print("Corrupted Data")
        return None



if __name__ == '__main__':
    
    minInterval = 30
    defInterval = minInterval
    MINUTES_TO_SECONDS = 60

    parser = argparse.ArgumentParser(description='Get value of stock with regular interval')
    parser.add_argument("company_symbol",
        help="Specify the symbol name of company")
    parser.add_argument("-i", "--interval", type=check_negative,
        help="Interval for regular checking in minutes. Default values is {}. Minimum value is {}".format(defInterval, minInterval))

    args = parser.parse_args()

    companySymbol = args.company_symbol

    if args.interval:
        interval = int(args.interval)
    else:
        interval = defInterval

    if interval < minInterval:
        interval = minInterval

    print("")
    print("Getting stock of {} with regular interval {} minutes".format(companySymbol, interval))
    print("")

    lastStockValue = 0
    firstTime = True

    while True:
        currStockValue = getStockValue(companySymbol)

        if currStockValue is None:
            print("error Happening...")
            print("program Quitting")
            break
        else:
            if currStockValue[1] < lastStockValue:
                status = "[DOWN]"
            elif currStockValue[1] > lastStockValue:
                status = "[UP]"
            else:
                status = "[EQUAL]"

            nowStr = time.strftime('%Y-%m-%d %H:%M')

            if firstTime:
                status = ""
                firstTime = False

            print("{} | {} | {}".format(nowStr, currStockValue[1], status))

            lastStockValue = currStockValue[1]

        time.sleep(interval * MINUTES_TO_SECONDS)