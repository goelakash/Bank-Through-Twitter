import httplib, urllib, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '91282cc98ef2479b90d4e83d3d808b79',
    'bearer':'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjdXN0b21lcklkIjoiNTcyZGJjYzlmZDNlNWQ2MDI1MTgwYTBlIiwicm9sZSI6InVzZXIiLCJwcmltYXJ5U3Vic2NyaWJlcktleSI6IjkxMjgyY2M5OGVmMjQ3OWI5MGQ0ZTgzZDNkODA4Yjc5IiwiaWF0IjoxNDYyNjIxMjg3fQ.ExCriM6tC4D--guj7dnG1ThLEa2HJpuJ0EuiTCDsh1A'
}

params = urllib.urlencode({
})

try:
    conn = httplib.HTTPSConnection('bluebank.azure-api.net')
    conn.request("GET", "/api/v0.6.3/customers", "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))
