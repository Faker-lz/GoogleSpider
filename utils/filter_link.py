"""
:
@author: lingzhi
* @date 2021/10/9 21:02
"""
from urllib.parse import urlparse, parse_qs
from feapder.utils.log import log


def filter_link(link):
    """
    Returns None if the link doesn't yield a valid result.
    Token from https://github.com/MarioVilas/google
    :return: a valid result
    """
    try:
        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse(link, 'http')
        if o.netloc:
            return link
        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]
            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc:
                return link
    # Otherwise, or on error, return None.
    except Exception as e:
        log.error('url解析错误!')
        return None