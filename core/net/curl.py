import pycurl
from io import BytesIO

class Curl:
    def __init__(self):
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.SSL_VERIFYPEER, 0)   
        self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)


    def perform(self, url):
        storage = BytesIO()
        self.curl.setopt(self.curl.WRITEFUNCTION, storage.write)
        self.curl.setopt(pycurl.URL, url)
        self.curl.perform()
        contents = storage.getvalue().decode('UTF-8')
        storage.close()
        return contents

    def close(self):
        self.curl.close()
