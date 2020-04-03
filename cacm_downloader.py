import requests
from os.path import exists
from os import remove
import tarfile

def data_downloader():
    """
     download the cacm.tar.gz from the given url, and uncompress it.
    """
    url = "http://dg3rtljvitrle.cloudfront.net/cacm.tar.gz"
    if not exists("cacm.tar.gz") and not exists('cacm'):
        cacm = requests.get(url)
        with open("cacm.tar.gz",'wb') as file:
            file.write(cacm.content)
    if not exists("cacm"):
        c = tarfile.open('cacm.tar.gz')
        c.extractall(path='cacm')
        c.close()
        remove(r"cacm.tar.gz")

