url = 'https://archives.nseindia.com/content/historical/EQUITIES/2020/FEB/cm27FEB2020bhav.csv.zip'
target_path = 'D:/alaska'
import requests
response = requests.get(url, stream=True)
handle = open(target_path, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        handle.write(chunk)
handle.close()
