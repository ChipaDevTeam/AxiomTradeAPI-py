from curl_cffi import requests

url = "https://axiom.trade/api/sol-balance"
payload = {"jsonrpc": "2.0", "id": 1, "method": "getBalance",
           "params": ["Cpxu7gFhu3fDX1eG5ZVyiFoPmgxpLWiu5LhByNenVbPb", {"commitment": "confirmed"}]}

response = requests.post(url, json=payload, impersonate="chrome136")
print(response.json()["result"]["value"])
print(response.status_code)
