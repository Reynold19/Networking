import requests
import os
chunk_size = 4096
filename = "bing.html"
document_url = "https://www.bing.com"
with requests.get(document_url, stream=True) as r:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size): 
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())

