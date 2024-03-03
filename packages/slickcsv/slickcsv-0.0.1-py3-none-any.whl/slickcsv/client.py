import os

import requests

from urllib.parse import urlparse

import json
import random

class SlickCSVWriter():
    path = "/results.csv"
    host = "http://localhost:8080"

    def __init__(self, url_path):
        res = urlparse(url_path)
        self.url = res.scheme + "://" + res.netloc
        self.path = res.path

    def __enter__(self):
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        pass

    def writerow(self, row_data):
        data = json.dumps({
            "path": self.path,
            "lines": [str(row_data)],
        })
        
        requests.post(self.host, data = data)

        print(data)

if __name__=="__main__":
    csv_path = "http://localhost:8080/syoung/sample.csv"
    with SlickCSVWriter(csv_path) as scsv:
        for i in range(100):
            scsv.writerow(["hello", "world", 16, "some", "data", random.randint(0,100)])
