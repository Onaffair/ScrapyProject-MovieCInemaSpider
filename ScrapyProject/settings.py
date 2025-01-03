# Scrapy settings for ScrapyProject project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.settings.default_settings import FEEDS

BOT_NAME = "ScrapyProject"

SPIDER_MODULES = ["ScrapyProject.spiders"]
NEWSPIDER_MODULE = "ScrapyProject.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "ScrapyProject (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:


headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'uuid_n_v=v1; uuid=8FDACE00A03F11EFB8546310D54B6F2217DB1665089D4A56B8E4A74D92A8D0AD; _lxsdk_cuid=1931bc9da25c8-07a774803b3189-26011951-1fa400-1931bc9da25c8; _lxsdk=8FDACE00A03F11EFB8546310D54B6F2217DB1665089D4A56B8E4A74D92A8D0AD; _ga=GA1.1.688149771.1731338034; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _csrf=dd7284c6210021360b0afceee236e7073278351d78c4543060dd590b3b5b2882; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1731747416,1731770496,1731772665,1731779249; HMACCOUNT=94AE80689864874E; __mta=210591402.1731338034555.1731770496925.1731779318553.31; _lxsdk_s=1933616451a-034-3f9-4c3%7C%7C10; _ga_WN80P4PSY7=GS1.1.1731779249.10.1.1731780653.0.0.0; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1731780653',
    'Pragma': 'no-cache',
    'Referer': 'https://www.maoyan.com/films/1393396',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "ScrapyProject.middlewares.ScrapyprojectSpiderMiddleware": 543,
# }


DOWNLOADER_MIDDLEWARES = {
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
}
PROXY_LIST = [
    'http://50.231.110.26:80',
    'http://68.71.241.33:4145',
    "http://101.71.143.237:8092",
    "http://136.226.233.109:10742",
    "http://130.193.123.34:5678",
    "http://101.231.64.89:8843",
    "http://194.147.33.5:8080",
    "http://168.119.141.135:80",
    "http://194.250.197.206:80"

]
PROXY_MODE = 0
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
RANDOMIZE_PROXY_ORDER = True

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "ScrapyProject.middlewares.ScrapyprojectDownloaderMiddleware": 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "ScrapyProject.pipelines.ScrapyprojectPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"




#间隔
DOWNLOAD_DELAY = 1

# 日志级别
LOG_LEVEL = 'ERROR'
