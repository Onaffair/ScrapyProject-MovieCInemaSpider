# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectionRefusedError, ConnectionDone, ConnectError, DNSLookupError

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# ScrapyProject/middlewares.py


class CaptchaDetectionMiddleware(RetryMiddleware):
    def __init__(self, settings):
        super(CaptchaDetectionMiddleware, self).__init__(settings)
        self.proxy_list = settings.getlist('PROXY_LIST')  # 从settings.py加载IP列表
        self.current_proxy_index = 0  # 当前使用的IP索引
        self.logger = None  # 初始化logger属性

    @classmethod
    def from_crawler(cls, crawler):
        # 从crawler中初始化中间件
        middleware = cls(crawler.settings)
        middleware.logger = crawler.spider.logger  # 初始化logger
        return middleware

    def get_next_proxy(self):
        """获取下一个可用的代理IP"""
        print(f'CaptchaDetectionMiddleware: 正在切换IP')
        if not self.proxy_list:
            return None

        # 切换到下一个IP
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return self.proxy_list[self.current_proxy_index]

    def process_response(self, request, response, spider):
        # print(f'CaptchaDetectionMiddleware: {request.url}')
        captcha_identifier = 'verify'
        if captcha_identifier in response.url or captcha_identifier in response.text:
            self.logger.warning(f'验证码检测到，正在切换IP: {request.url}')
            new_proxy = self.get_next_proxy()  # 获取下一个代理IP
            print(new_proxy)
            if new_proxy:
                request.meta['proxy'] = new_proxy  # 设置新的代理IP
                return self._retry(request, IgnoreRequest(), spider)  # 重试请求
            else:
                self.logger.error('没有可用的代理IP，无法切换')
                return response
        else:
            return response

    def process_exception(self, request, exception, spider):
        print("CaptchaDetectionMiddleware: 处理异常")
        if isinstance(exception, (DNSLookupError, TimeoutError, TCPTimedOutError, ConnectionRefusedError, ConnectionDone, ConnectError, TunnelError)):
            self.logger.warning(f'请求失败，正在切换IP: {request.url}')
            new_proxy = self.get_next_proxy()  # 获取下一个代理IP
            if new_proxy:
                request.meta['proxy'] = new_proxy  # 设置新的代理IP
                return self._retry(request, exception, spider)  # 重试请求
            else:
                self.logger.error('没有可用的代理IP，无法切换')
                return None


class ScrapyprojectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
class ScrapyprojectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
