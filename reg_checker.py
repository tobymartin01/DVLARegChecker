'''
-----INFORMATION-----
Python Script using DVLA api to gather detailed information on vehicles based on their reg plates. For instructions on use see below.

https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles

key:
x-api-key

body:
{ 
  "registrationNumber": "TE57VRN" 
}

example:
curl -L -X POST 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles' \
-H 'x-api-key: REPLACE WITH YOUR API KEY' \
-H 'Content-Type: application/json' \
-d '{"registrationNumber": "TE57VRN"}'

response:
{
  "artEndDate": "2025-02-28",
  "co2Emissions" : 135,
  "colour" : "BLUE",
  "engineCapacity": 2494,
  "fuelType" : "PETROL",
  "make" : "ROVER",
  "markedForExport" : false,
  "monthOfFirstRegistration" : "2004-12",
  "motStatus" : "No details held by DVLA",
  "registrationNumber" : "ABC1234",
  "revenueWeight" : 1640,
  "taxDueDate" : "2007-01-01",
  "taxStatus" : "Untaxed",
  "typeApproval" : "N1",
  "wheelplan" : "NON STANDARD",
  "yearOfManufacture" : 2004,
  "euroStatus": "EURO 6 AD",
  "realDrivingEmissions": "1",
  "dateOfLastV5CIssued": "2016-12-25"
}

from the above we take engineCpacity and fuelType

error responses:
400	Bad Request	- Bad Request
404	Not Found -	Vehicle Not Found
500	Internal Server Error -	Internal Server Error
503	Service Unavailable - Service Unavailable

-----HOW TO USE-----
'''

import requests
import numpy as np
import csv


#imports dataset and converts to a list. [change reg_ist.csv to file name]
with open('input.csv') as f:
    reader = csv.reader(f)
    data = list(reader)

url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"

arr = ['reg', 'engineSize', 'fuelType', 'RevenueWeight']

for i in range(len(data)):

  reg = ((str((data[i]))).strip("[]'"))

  payload_start = "{\n\t\"registrationNumber\": \""
  payload_reg = reg
  payload_end = "\"\n}"
  payload = payload_start + payload_reg + payload_end
  headers = {
    'x-api-key': '', 
    'Content-Type': 'application/json'
  }

  # ------- INSERT API KEY ABOVE--------

  response = requests.request("POST", url, headers=headers, data = payload)

  #takes api output and converst to readable
  output = response.text

  #takes the api response and converts into a string, then splits at ',' into a list of values
  outputFormatted= str(output)
  outputFormatted= output.split(',')



  arr2 = ['','','','']

  print (i, reg)
  print(outputFormatted)

  for i in range(len(outputFormatted)):
      
      if "errors" in outputFormatted[i]:
         arr2 = [reg,'error','error','error']
         break
      
      if "registrationNumber" in outputFormatted[i]:
        arr2[0] = ((outputFormatted[i]).replace('{\"registrationNumber\":',''))

      if "engineCapacity" in outputFormatted[i]:
        arr2[1] = ((outputFormatted[i]).replace('\"engineCapacity\":',''))

      if "fuelType" in outputFormatted[i]:
        arr2[2] = ((outputFormatted[i]).replace('\"fuelType\":',''))

      if "revenueWeight" in outputFormatted[i]:
        arr2[3] = ((outputFormatted[i]).replace('\"revenueWeight\":',''))


  print(arr2)
  arr = np.vstack([arr, arr2])


#change 'test.csv' to whatever you want the file to be called
with open('output.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in range(len(arr)):
        writer.writerow(arr[i])


