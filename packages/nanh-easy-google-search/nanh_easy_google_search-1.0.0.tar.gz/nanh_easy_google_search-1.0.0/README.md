# Google搜索工具
Google官方出的搜索工具无法直接使用代理，就对官方的进行了改动与精简。
根据关键字进行搜索，通过 `BeautifulSoup` 对内容进行解析，并返回搜索的连接地址
项目依赖：
- beautifulsoup4
- Requests
- urllib3

# 安装
## 源码安装
```bash
git clone https://github.com/877007021/easy_google_search.git
pip install -r requirements.txt

```

## pip 安装
```bash
pip install nanh-easy-google-search==0.0.1
```

# 示例
``` python
from nanh_easy_google_search.google import search
# or from google import search  
  
proxies = {  
    'http': 'http://127.0.0.1',  
    'https': 'http://127.0.0.1',  
}  
  
search_link_list = search("easy_google_search", proxies=proxies)  
[print(link) for link in search_link_list]
```
如果此工具有任何问题或错误，请提出问题。