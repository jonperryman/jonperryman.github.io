import http.client
host = "localhost"
port = 8000
conn = http.client.HTTPSConnection(host)
conn.request("GET", "/xxx", headers={"Host": host})
response = conn.getresponse()
print(response.status, response.reason)
if response.status != 200:
    print("http requests failed status: ", response.status, " reason: ", response.reason)
else:
    data = response.read()
    print("response=", data)
print("all done")