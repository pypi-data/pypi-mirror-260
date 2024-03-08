from google import search

proxies = {
    'http': 'http://127.0.0.1',
    'https': 'http://127.0.0.1',
}

search_link_list = search("nanh_easy_google_search", proxies=proxies)
[print(link) for link in search_link_list]
