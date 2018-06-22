from api import * 
from datetime import date
import datetime  
import schedule
import time 
import threading 
import json 
from email.parser import Parser
parser = Parser()


account = []



   

#Queries Shipment IMEIs 
query = sf.query("SELECT Id, zkusps__lastTrackUpdateTime__c, zkusps__shipmentNotes__c, Name, zkusps__trackingNumber__c, zkusps__toAccount__c FROM zkusps__Shipment__c WHERE zkusps__replyPostage__c = True AND zkusps__isDelivered__c = True AND zkusps__lastTrackUpdateTime__c >= LAST_WEEK")



#Formats query for json 
jsonInput = query  
jsonForFile = json.dumps(jsonInput, sort_keys=True,
                  indent=4, separators=(',', ': '))
json2 = json.loads(jsonForFile)



#Declares todays date
today = date.today().isoformat()



shipmentNotesIMEIs = [] #Declares array var 
for x in json2['records']:
  
  print ''
  print 'New iteration'
  print ''
  
  
  #Shipment section 
  print 'Shipment section'
  print x['zkusps__shipmentNotes__c']
  #shipmentNotesIMEI = x['zkusps__shipmentNotes__c'].split('\n')
  shipmentNotesIMEI = x['zkusps__shipmentNotes__c']
  #shipmentNotesIMEI = shipmentNotesIMEI.split(', ') #Uncomment for script to work
  #shipmentNotesIMEI = shipmentNotesIMEI.split('\






  if ',' in shipmentNotesIMEI: 
    shipmentNotesIMEI = shipmentNotesIMEI.split(', ')
  else: 
     shipmentNotesIMEI = shipmentNotesIMEI.splitlines()



  print "Shipment Notes IMEI"
  print shipmentNotesIMEI #Prints ShipmentNotesIMEI array to check contents 
      

  accountRaw = x['zkusps__toAccount__c'] #Pulls account number 
  acctIDstripe = accountRaw[0:15] #Strips unrelated end letters from account number 
  acctIDparens = "'" + acctIDstripe + "'" #Places '' around Account number to query as a string in SFDC
  print 'Account ID'
  print acctIDparens #Prints Accout number for check 
  print ''
  
  ShipmentIMEIs = shipmentNotesIMEI #Simplifies name of var name 
  print 'Shipment IMEIs variable' 
  print ShipmentIMEIs #Var visual check 
  
  #Return section 
  print 'Return section'
  #accountIMEI = { 
  account = sf.query("SELECT Incoming_IMEI__c, ID FROM Return__c WHERE Account__c = %s AND Stage__c != 'Returned Closed'"  % acctIDparens) #Queries return 
  print 'Return Json'
  print account #
  
  #formats json  
  returnJsonDumps =  json.dumps(account, sort_keys=True,
                  indent=4, separators=(',', ': '))
  returnJsonLoads = json.loads(returnJsonDumps)
  returnIMEIs = returnJsonLoads['records'] #Pulls section containing IMEI  

  #Return IMEIs
  #Queries for Return Closed returns stop script 
  try:

    returnId = returnIMEIs[0]['Id'] #Pull return ID
    returnId = returnId[0:15] #Strips unrelated numbers from the end of ID 
    print 'return ID'
    print returnId #Prints ID for visual check 



    print 'Try section: print return IMEIs'  
    returnIMEIs1 = returnIMEIs[0]['Incoming_IMEI__c'] #Pulls Return IMEIs string from json 
    #print returnIMEIs1
    try: 
      returnIMEIs = returnIMEIs1.split(', ') #Parses string into array
      print returnIMEIs #Visual check of var 
    except AttributeError: 
      pass   
  
    try: 
      returnIMEIs = returnIMEIs1.split('\r\n')
      print returnIMEIs #Visual check of var
    except AttributeError:
      pass 

    '''
    try: 
      print returnIMEIs #Visual check of var
      if type(returnIMEIs1) is None: 
        print "Return IMEI is type None" 
      elif '\r\n' in returnIMEIs1: #If return and newline
        print 'Return IMEIs contain newline and return'
        returnIMEIs = returnIMEIs1.split('\r\n') #Splits return IMEI string 
        print returnIMEIs  
      else:o
        print 'None' 
       
    except AttributeError: 
      pass
    '''
  except IndexError: 
    print 'Try section: Not print return IMEIs' #String is empty 
    pass
  #continue

  print 'Return IMEIs' 
  print  returnIMEIs #Visual check of array 
  
  Return = returnIMEIs #Renaming var  
  print 'Return'  
  print Return #Visual check of array 


  print ''
  print 'Compare section'  
  for a in ShipmentIMEIs: #Parses item in array 
    print 'Shipment IMEIs' 
    print a 
    #for c in b: 
      #print c 

  for x in Return: #Parses item in array  
    print 'Return IMEIs'  
    print x


  #Will count the number of matching IMEI to determine if Return should be closed 
  deviceNum = len(ShipmentIMEIs) #Measure number of items in shipment array 
  deviceNumConfirm = 0 #init infirm number
 

  for a in ShipmentIMEIs: #Iterate through Shipment IMEI 
    print 'Shipment IMEIs' 
    print a
    #for c in b: 
      #print c 

    for x in Return: #Iterate through Return IMEI 
      global deviceNumConfirm
      print 'Return IMEIs'  
      print x 
      if x == a: #Compares Shipment and Return IMEIs 
        print  
        print 'IMEIs are equal'  
        deviceNumConfirm = deviceNumConfirm + 1 #Iterates matches up 
      else: 
        print 'No equal IMEIs' 
  print ''
  print "Device Number"
  print deviceNum
  print "Device Number Confirm"
  print deviceNumConfirm
  print ''



  #Updates Return 
  if deviceNumConfirm == deviceNum: #If arrays are equal 

    returnUpdate = sf.Return__c.update(returnId,  {'Stage__c' : 'Returned closed'})
    closeDate = sf.Return__c.update(returnId, {'Close_date__c' : today})


     
  #print  
  print ''
  print ''
  print '' 
   
print ''
print account 
print ''

