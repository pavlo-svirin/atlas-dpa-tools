import pycurl

class Curl:
    def __init__(self):
        self.storage = BytesIO()
        self.curl = pycurl.Curl()
        self.curl.setopt(pycurl.SSL_VERIFYPEER, 0)   
        self.curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        self.curl.setopt(self.curl.WRITEFUNCTION, storage.write)


    def perform(self, url):
        curl.setopt(pycurl.URL, url)
        curl.perform()
        curl.close()
        return storage.getvalue().decode('UTF-8')

