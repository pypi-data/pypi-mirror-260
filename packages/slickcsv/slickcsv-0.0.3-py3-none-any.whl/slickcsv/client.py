import os

import requests
from requests.adapters import HTTPAdapter, Retry

from urllib.parse import urlparse

import json
import random

class SlickCSVWriter():
    retries = 5
    url = "http://localhost:8080/results.csv"

    def __init__(self, url_path):
        self.url = url_path
        
    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass

    def writerow(self, row_data):

        # We expect row_data to be a python list of data to be
        # written.  We convert it all to a comma separated string.
        final = []
        for elem in row_data:
            final.append(str(elem))
        
        data = json.dumps({
            "lines": [",".join(final)],
        })

        s = requests.Session()
        retries = Retry(total=self.retries, backoff_factor=1, status_forcelist=[ 503 ])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        s.post(self.url, data = data)
        
if __name__=="__main__":
    #csv_path = "http://localhost:8080/Users/jhoffman/Desktop/sample.csv"
    csv_path = "http://localhost:8080/Users/jhoffman/Desktop/test/results/sample.csv"
    with SlickCSVWriter(csv_path) as scsv:
        for i in range(25):
            scsv.writerow(["hello", "world", 16, "some", "data", random.randint(0,100)])
