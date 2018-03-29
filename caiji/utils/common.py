import hashlib

def get_md5(url):#unicode 没有md5
    if isinstance(url,str):#在python3中没有unicode关键词了,用str
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()
