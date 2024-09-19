#######################################################################################
# This script accesses data for the FoxESS Solar and Battery system from the
# FoxESS cloud using the owners API Key (configurable).
# The script obtains 6 key instantaneous numbers:
# 1. Solar Power being generated
# 2. Power imported from the Grid connection
# 3. Power exported to the Grid connection
# 4. Power being sent to/from the Battery
# 5. Current Battery State of Charge (SoC)
# 6. Power being consumed by the house (various loads)
# 
# Note it is possible to obtain more information than just these numbers from the FoxESS Cloud
# but, on the standard "free tier" you are only allowed 1440 calls per day (enough for 1 per minute)
# to obtain the data required above requires 5 different explicit calls, plus one implicit call for
# authentication, so each time it runs this script uses 6 of the available calls.  As such, on the free
# tier, it can only be executed once every 5 minutes.  This is controlled via a cron job.
# If you modify the script to obtain additional information you may need to trade that off against
# how fequently you call it, or you will run out of accesses before the end of the day
######################################################################################## 
# 
# #!/usr/bin/python3

import os
import socket
import logging
from configparser import ConfigParser
import json

from datetime import datetime
import foxesscloud.openapi as f

# additional imports for foxess async api
import asyncio

debug = True

async def main():
    """loxberry plugin for foxess API sends every 5 minutes the actual
    power production and power consumption values to the miniserver"""
    # create file strings from os environment variables
    lbplog = os.environ['LBPLOG'] + "/foxess/foxess.log"
    lbpconfig = os.environ['LBPCONFIG'] + "/foxess/plugin.cfg"
    lbsconfig = os.environ['LBSCONFIG'] + "/general.cfg"
    #print (lbplog)
    #print (lbsconfig)

    # creating log file and set log format
    logging.basicConfig(filename=lbplog,level=logging.INFO,format='%(asctime)s: %(message)s ')
    #logging.info("<INFO> initialise logging...")
    # open config file and read options
    try:
        cfg = ConfigParser()
        #global_cfg = ConfigParser()
        cfg.read(lbpconfig)
        #global_cfg.read(lbsconfig)
    except:
        logging.error("<ERROR> Error parsing config files...")

    #define variables with values from config files
    apiKey = cfg.get("FOXESS", "API_KEY")
    serial = cfg.get("FOXESS", "SERIAL")
    #print (apiKey)
    #print (serial)
    f.api_key = apiKey
    f.device_sn = serial
    f.time_zone = "Europe/London"
    f.residual_handling = 1
    
    # comment for local debugging
    miniserver = cfg.get("MINISERVER", "IPADDRESS")
    udp_port = int(cfg.get("MINISERVER", "PORT"))
    # uncomment for local debugging
    #miniserver = "127.0.0.1" 
    #udp_port = 15555
    #print (miniserver)
    #print (udp_port)
    # Get the data as dictionary and as json
    # Note calls to f.get_real([comma seprated value list]) returns a large python list with a directory structure for each value 
    # as the nth element of the list
    # to minimise the number of accesses used with each cycle, we make one call only that returns multiple values
    # Also to simplify the Loxone configuration we will combine grid import and grid export into a single signed number
    # and do the same with battery charge and discharge power values before passing the output to the miniserver
    # To do that we need to make one call to f.get_real with a complex array as follows
    # ['pvPower','gridConsumptionPower','feedinPower','loadsPower','batChargePower','batDischargePower','SoC']
    try:
        myvalues = f.get_real(['pvPower','gridConsumptionPower','feedinPower','loadsPower','batChargePower','batDischargePower','SoC'])
        print (f"My Values {myvalues}")
        mypvpd = myvalues[0]
        mygrdd = myvalues[1]
        myexpd = myvalues[2]
        myldpd = myvalues[3]
        mybtcd = myvalues[4]
        mybtdd = myvalues[5]
        mysocd = myvalues[6]
    
        pvpwr = mypvpd["value"]
        gdpwr = mygrdd["value"]       
        gdexp = myexpd["value"]       
        ldpwr = myldpd["value"]
        btchg = mybtcd["value"]
        btdis = mybtdd["value"]
        btsoc = mysocd["value"]
        
        if btdis > 0: 
            batpwr = btdis
        else:
            batpwr = -btchg
        
        if gdpwr > 0:
            grdpwr = gdpwr
        else:
            grdpwr = -gdexp
        
        #print ("done getting data")
        
        #Now construct message from received data
        # construct dictionary
        now = datetime.now()
        currentdate = now.strftime("%d-%m-%Y")
        currenttime = now.strftime("%H:%M:%S")
        
        ldpwr = ldpwr.__round__(2)
        grdpwr = grdpwr.__round__(2)
        pvpwr = pvpwr.__round__(2)
        batpwr = batpwr.__round__(2)
        btsoc = btsoc.__round__(2)
    
        msg = {
            'dat':currentdate,
            'tim':currenttime,
            'con':ldpwr,
            'grd':grdpwr,
            'gen':pvpwr,
            'bat':batpwr,
            'soc':btsoc
             }
        
        #Convert the data to a json string
        message = json.dumps(msg)
        logging.info("<INFO> Value: %s" % message)
        #print (message)
        #now send it
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Send the JSON string to the specified IP and port
            sock.sendto(message.encode(), (miniserver, udp_port))
            #print(f"Sent UDP packet to {miniserver}:{udp_port}: {message}")
        finally:
            # Close the socket
            sock.close()
    except:
        logging.error("<ERROR> Failed to execute API call...")
        msg = None


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    