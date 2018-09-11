from hashlib import md5
def handle_by_md5(link):
    '''
    将链接进行md5处理
    :param link:
    '''
    if isinstance(link,str):
        link = link.encode('utf-8')
    md = md5()
    md.update(link)
    return md.hexdigest()

def handle_blank(value):
    try:
        value = value.strip()
    except:
        return value
    else:
        if '/' in value:
            value = value.strip('/')
            value = value.strip()
    return value

def handle_job_city(value):
    value = value.split('\n')
    value = [i.strip() for i in value if '查看地图' not in i]
    return ''.join(value)


if __name__ == '__main__':
    link = handle_by_md5('www.baidu.com')
    print(link)

