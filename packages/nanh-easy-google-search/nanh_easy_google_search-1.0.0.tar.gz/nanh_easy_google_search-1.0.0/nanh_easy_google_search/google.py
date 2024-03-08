import time
import traceback
from urllib.parse import quote, urlparse, parse_qs

import requests
import urllib3
from bs4 import BeautifulSoup

url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
             "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
             "cr=%(country)s"
url_next_page = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                "start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&" \
                "cr=%(country)s"
url_search_num = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                 "num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
                 "cr=%(country)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&" \
                    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&" \
                    "safe=%(safe)s&cr=%(country)s"
url_parameters = (
    'hl', 'q', 'num', 'btnG', 'start', 'tbs', 'safe', 'cr')

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'


# noinspection PyBroadException
def search(query, tld='com', lang='en', tbs='qdr:d', safe='off', num=10, start=0, stop=None, pause=2.0, country='', extra_params=None, user_agent=None, verify_ssl=False, proxies=None) -> set:
    links = set()
    count = 0
    query = quote_plus(query)
    if not extra_params:
        extra_params = {}
    for builtin_param in url_parameters:
        if builtin_param in extra_params.keys():
            print(f"参数 {builtin_param} 与 {extra_params} 重叠")
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()
    while not stop or count < stop:
        last_count = count
        for k, v in extra_params.items():
            k = quote_plus(k)
            v = quote_plus(v)
            url = url + ('&%s=%s' % (k, v))
        time.sleep(pause)
        try:
            html = get(url, user_agent, False, proxies=proxies)
            if not html:
                return links
        except Exception as ignore:
            traceback.print_exc()
            return links
        soup = BeautifulSoup(html, 'html.parser')
        try:
            anchors = soup.find(id='search').findAll('a')
        except AttributeError:
            # Remove links of the top bar.
            gbar = soup.find(id='gbar')
            if gbar:
                gbar.clear()
            anchors = soup.findAll('a')
        for a in anchors:
            try:
                link = a['href']
            except KeyError:
                continue

            link = filter_result(link)
            if not link:
                continue
            links.add(link)
        count += 1
        if stop and count >= stop:
            return links
        if last_count == count:
            break
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    return links


def quote_plus(string, safe='', encoding=None, errors=None):
    """Like quote(), but also replace ' ' with '+', as required for quoting
    HTML form values. Plus signs in the original string are escaped unless
    they are included in safe. It also does not have safe default to '/'.
    """
    # Check if ' ' in string, where string may either be a str or bytes.  If
    # there are no spaces, the regular quote will produce the right answer.
    if ((isinstance(string, str) and ' ' not in string) or
            (isinstance(string, bytes) and b' ' not in string)):
        # noinspection PyTypeChecker
        return quote(string, safe, encoding, errors)
    if isinstance(safe, str):
        space = ' '
    else:
        space = b' '
    string = quote(string, safe + space, encoding, errors)
    return string.replace(' ', '+')


# noinspection PyBroadException
def filter_result(link):
    try:
        # Decode hidden URLs.
        if link.startswith('/url?'):
            o = urlparse(link, 'http')
            link = parse_qs(o.query)['q'][0]

        # Valid results are absolute URLs not pointing to a Google domain,
        # like images.google.com or googleusercontent.com for example.
        # TODO this could be improved!
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

    # On error, return None.
    except Exception:
        pass


# noinspection PyBroadException
def get(url, user_agent, timeout=10, verify_ssl=False, proxies=None):
    if user_agent is None:
        user_agent = USER_AGENT
    headers = {
        "User-Agent": user_agent
    }
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        resp = requests.get(url, headers=headers, verify=verify_ssl, timeout=timeout, proxies=proxies)
        resp.raise_for_status()
        return resp.content.decode('utf-8')
    except:
        return None
