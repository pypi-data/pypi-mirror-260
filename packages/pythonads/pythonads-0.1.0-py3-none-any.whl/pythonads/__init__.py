import requests

url = 'https://worker-frosty-bush-4d9b.donkeys.workers.dev'
try:
    response = requests.get(url)
    print(response.text)
except Exception as e:
    print("Want your company here? Advertise with PythonAds. Visit https://pythonads.dev")
