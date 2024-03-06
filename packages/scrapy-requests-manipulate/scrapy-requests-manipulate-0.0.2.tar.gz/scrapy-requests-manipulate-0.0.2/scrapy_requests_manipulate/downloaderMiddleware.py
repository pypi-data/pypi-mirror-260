# -*- coding: utf-8 -*-

import requests
from scrapy import signals
from scrapy.http import HtmlResponse, TextResponse
from twisted.internet.threads import deferToThread
from twisted.internet import defer
from twisted.internet.error import (
    ConnectError,
    ConnectionDone,
    ConnectionLost,
    ConnectionRefusedError,
    DNSLookupError,
    TCPTimedOutError,
    TimeoutError,
)
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
from scrapy_requests_manipulate.settings import *
import random
import logging
logger = logging.getLogger('RequestsDownloaderMiddleware')
import json


class RequestsDownloaderMiddleware:

    EXCEPTIONS_TO_RETRY = (
        defer.TimeoutError,
        TimeoutError,
        DNSLookupError,
        ConnectionRefusedError,
        ConnectionDone,
        ConnectError,
        ConnectionLost,
        TCPTimedOutError,
        ResponseFailed,
        IOError,
        TunnelError,
    )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        settings = crawler.settings
        s = cls()
        cls.retry_enabled = settings.getbool('RETRY_ENABLED')
        cls.max_retry_times = settings.getint('RETRY_TIMES')
        cls.retry_http_codes = set(int(x) for x in settings.getlist('RETRY_HTTP_CODES'))
        cls.priority_adjust = settings.getint('RETRY_PRIORITY_ADJUST')
        cls.raw_response_type = settings.get('RAW_RESPONSE_TYPE', RAW_RESPONSE_TYPE)
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def _retry(self, request, reason, spider):

        if not self.retry_enabled:
            return None

        retry_times = request.meta.get('retry_times', 0) + 1
        max_retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            max_retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retry_times <= max_retry_times:
            logger.debug("Retrying %(request)s (failed %(retry_times)d times): %(reason)s",
                         {'request': request, 'retry_times': retry_times, 'reason': reason},
                         extra={'spider': spider})
            new_request = request.copy()
            new_request.meta["retry_times"] = retry_times
            new_request.dont_filter = True
            new_request.priority = request.priority + self.priority_adjust

            if callable(reason):
                reason = reason()
            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return new_request
        else:
            stats.inc_value('retry/max_reached')
            logger.error("Gave up retrying %(request)s (failed %(retry_times)d times): %(reason)s",
                         {'request': request, 'retry_times': retry_times, 'reason': reason},
                         extra={'spider': spider})
            return None

    def _process_request(self, request, spider):
        method = request.method
        url = request.url
        headers = request.headers.to_unicode_dict()
        params = request.meta.get('params', None)
        data = request.meta.get('data', None)
        cookies = request.meta.get('cookies', None)
        json_ = request.meta.get('json', None)
        if params:
            try:
                params = json.loads(params)
            except:
                pass
        if data:
            try:
                data = json.loads(data)
            except:
                pass
        if cookies:
            try:
                cookies = json.loads(cookies)
            except:
                pass
        if json_:
            try:
                json_ = json.loads(json_)
            except:
                pass
        proxy_ = request.meta.get('proxy_', None)
        try:
            proxy_ = json.loads(proxy_)
        except:
            pass
        if isinstance(proxy_, list):
            proxy = random.choice(proxy_)
            proxies = {
                'https': proxy,
                'http': proxy
            }
        else:
            proxies = proxy_
        try:
            response = requests.request(method=method, url=url, params=params, data=data,
                                       headers=headers, cookies=cookies,
                                       json=json_, proxies=proxies)
        except Exception as e:
            return None
        if self.raw_response_type == 'HtmlResponse':
            new_response = HtmlResponse(url=response.url, status=response.status_code, headers=response.headers,
                                        body=response.text, request=request, encoding='utf-8')
        elif self.raw_response_type == 'TextResponse':
            new_response = TextResponse(url=response.url, status=response.status_code, headers=response.headers,
                                        body=response.text, request=request, encoding='utf-8')
        else:
            logger.error(f'RAW_RESPONSE_TYPE must be HtmlResponse or TextResponse, but {self.raw_response_type} was given')
            return None
        return new_response

    def process_request(self, request, spider):
        logger.debug('requests handle request %s', request)
        return deferToThread(self._process_request, request, spider)

    def process_response(self, request, response, spider):
        if request.meta.get("dont_retry", False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) and not request.meta.get(
                "dont_retry", False
        ):
            return self._retry(request, exception, spider)

    def spider_opened(self, spider):
        spider.logger.info("RequestsDownloaderMiddleware enabled")

    def spider_closed(self, spider):
        spider.logger.info("Spider closed: %s" % spider.name)
