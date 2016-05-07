import httplib, urllib, base64, json, geocoder

tdict =     {
  "toAccountNumber":"6000018",
  "toSortCode":"839999",
  "paymentReference":"string",
  "paymentAmount": 10.0
}

headers = {
    # Request headers

    'Content-Type':'application/json',
    'Ocp-Apim-Subscription-Key':'91282cc98ef2479b90d4e83d3d808b79',
    'bearer':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjoiNTcyZGJjYzlmZDNlNWQ2MDI1MTgwYTBlIiwicm9sZSI6InVzZXIiLCJwcmltYXJ5U3Vic2NyaWJlcktleSI6IjkxMjgyY2M5OGVmMjQ3OWI5MGQ0ZTgzZDNkODA4Yjc5IiwiaWF0IjoxNDYyNjIxMjg3fQ.ExCriM6tC4D--guj7dnG1ThLEa2HJpuJ0EuiTCDsh1A'
}

# customer_id = '572dbcc9fd3e5d6025180a0e'

# acc_balance = 0
# acc_id = '572dbccafd3e5d6025180a10'
# acc_no = '6000018'

# acc_balance = 14389.1
# acc_id = '572dbcc9fd3e5d6025180a0f'
# acc_no = '2000018'

g = geocoder.google("London, UK")
lat, lng = g.latlng

params = urllib.urlencode({
    'lat':lat,
    'lng':lng,
    'radius':"1000"
})


try:
    conn = httplib.HTTPSConnection('bluebank.azure-api.net')
    conn.request("POST", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/payments", json.dumps(tdict), headers)
    # conn.request("GET", "/api/v0.6.3/customers/572dbcc9fd3e5d6025180a0e","",headers)
    # conn.request("GET", "/api/v0.6.3/customers/572dbcc9fd3e5d6025180a0e/accounts","",headers)
    # conn.request("GET", "/api/v0.6.3/branches/near?%s" % params,"",headers)
    # conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f","",headers)
    # conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/payments","",headers)
    # conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/transactions","",headers)
    # conn.request("GET", "/api/v0.6.3/accounts/572dbcc9fd3e5d6025180a0f/transactions?%s"% params,"",headers)
    print("Sent Request")
    response = conn.getresponse()
    print(response.read())
    # data = json.loads(response.read())[0]
    # for x in data:
    #     print(x+": "+data[x])
    ### transaction management system
    # print(conn.getresponse().read())
    # response = conn.getresponse().read().split("}")
    # response = response[:-1]
    # for i in range(len(response)):
    #     response[i] = response[i][1:]   #[{...}, {...}, {...}]
    #     response[i] = response[i]+'}'
    # for i in range(len(response)):
    #     response[i] = json.loads(response[i])
    #     print(response[i])



    # print("Got response")
    # print(dir(response))
    # print(response['msg'])

    # for x in response:
    #     print(x)
    # print(data)
    conn.close()
except Exception as e:
    #print(e)
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
