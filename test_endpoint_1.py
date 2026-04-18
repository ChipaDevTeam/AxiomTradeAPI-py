import requests

url = "https://api3.axiom.trade/new-trending-v2?timePeriod=1h&v=1776512193004"

data = requests.get(url)
print(data.content)