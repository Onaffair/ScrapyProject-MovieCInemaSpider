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
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'https://www.maoyan.com',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "ScrapyProject.middlewares.ScrapyprojectSpiderMiddleware": 543,
# }


DOWNLOADER_MIDDLEWARES = {
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
    "ScrapyProject.middlewares.CaptchaDetectionMiddleware": 543,
    'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware': None,
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

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


#间隔
DOWNLOAD_DELAY = 1

# 日志级别
LOG_LEVEL = 'ERROR'
