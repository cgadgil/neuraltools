import httplib, urllib, json

xd = json.dumps([[1.0, 2.0, 3.0], [2.1, 4.4, 5.9], [3.6, 5.9, 8.2], [5.1, 9.3, 14.6]])
yd = json.dumps([11.2, 24.1, 29.2, 40.8])
dd = urllib.urlencode({'xData': xd, 'yData': yd})
params = dd
conn = httplib.HTTPConnection("localhost:8080")
conn.request("POST", "/fundamental/regression", params, headers)

