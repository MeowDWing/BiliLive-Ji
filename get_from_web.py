import requests
import re
import urllib.request as ure
import os
import iosetting as ios


def get_dl_files(url: str='None',name: str='rid') -> str:
    """

    :param url:str the url link
    :return (str) -1:no url input; -2: error url; file_name: file_name has been downloaded
    """
    if url != 'None':
        pwd = os.getcwd()
        if not os.path.exists('livecover'):
            os.mkdir('livecover')
        print(url)
        file_name = url.split('/')[-1]
        try:
            ure.urlretrieve(url=url, filename='./livecover/'+file_name)
            ios.print_set("下载完成", tag='SUCCESS')
        except ValueError:
            ios.print_set("Wrong URL", tag='WARNING')
            return '-2'
    else:
        ios.print_set('Wrong URL', tag='WARNING')
        return '-1'

    pwd = os.path.join(pwd, 'livecover\\')
    file_name = pwd + file_name
    return file_name


