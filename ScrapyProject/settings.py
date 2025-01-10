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

cookies = {
    '_ga': 'GA1.1.427435205.1732029469',
    '_lxsdk_cuid': '19345005032c8-0452f97f12a0d1-26011951-1fa400-19345005032c8',
    'uuid_n_v': 'v1',
    'uuid': '2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123',
    '_lxsdk': '2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123',
    '_csrf': 'f9b7af475b9c18f3ac7a859b90488ad551fe346db97e98a4959c00667efabdb6',
    'Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533': '1736498191,1736512370,1736512467,1736512484',
    'HMACCOUNT': '0AF1B23D10885BE0',
    '_ga_WN80P4PSY7': 'GS1.1.1736512369.55.1.1736512486.0.0.0',
    'Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533': '1736512486',
    '__mta': '242479805.1732029470408.1736512485481.1736512486203.50',
    '_lxsdk_s': '1945033f41b-806-941-712%7C%7C10',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga=GA1.1.427435205.1732029469; _lxsdk_cuid=19345005032c8-0452f97f12a0d1-26011951-1fa400-19345005032c8; uuid_n_v=v1; uuid=2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123; _lxsdk=2D3DE750C96B11EF8BF5E789F57BC8028090C83F046C49CF99937114F4A20123; _csrf=f9b7af475b9c18f3ac7a859b90488ad551fe346db97e98a4959c00667efabdb6; Hm_lvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1736498191,1736512370,1736512467,1736512484; HMACCOUNT=0AF1B23D10885BE0; _ga_WN80P4PSY7=GS1.1.1736512369.55.1.1736512486.0.0.0; Hm_lpvt_e0bacf12e04a7bd88ddbd9c74ef2b533=1736512486; __mta=242479805.1732029470408.1736512485481.1736512486203.50; _lxsdk_s=1945033f41b-806-941-712%7C%7C10',
    'Referer': 'https://www.maoyan.com/films',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
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

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOADER_MIDDLEWARES.update({
    "ScrapyProject.middlewares.CaptchaDetectionMiddleware": 543,
})


#间隔
DOWNLOAD_DELAY = 1

# 日志级别
LOG_LEVEL = 'ERROR'
