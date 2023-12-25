import requests


response = requests.get('https://api.binance.com/api/v3/depth?symbol=BTCUSDT&limit=1')
print('Status code =', response.status_code)
data = response.json()
print('data:', data)
print('Current BTC price =', data['asks'][0][0])
