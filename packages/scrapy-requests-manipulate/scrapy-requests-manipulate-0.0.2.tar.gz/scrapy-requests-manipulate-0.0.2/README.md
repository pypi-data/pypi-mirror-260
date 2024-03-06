# Scrapy Requests Downloader Middleware

This package will make scrapy support requests. Everything is same with requests.

## Installation

```shell script
pip3 install scrapy-requests-manipulate
```

## Usage

After add this middleware, all requests will be sent by requests.

The usage is very simple, for request, specify params in meta.


### Settings for Request

```python
params = {
    'key1': 'value1',
    'key2': 'value2',
}
data = {
    'key1': 'value1',
    'key2': 'value2',
}
# turn cookie jar into dict, and remove the " mark, use ' mark
cookies = {
    'key1': 'value1',
    'key2': 'value2',
}
payload = {
    'key1': 'value1',
    'key2': 'value2'
}
proxy_ = 'http://username:password@ip:port' # https also works
or 
proxy_ = [
    'http://username:password@ip:port',
    'http://username:password@ip:port',
] # if the type of proxy is list, every request will get a random proxy in the list

meta_data = {
    'params': params,
    'data': data,
    'cookies': cookies,
    'json': payload,
    'proxy_': proxy_
}
or 
meta_data = {
    'params': json.dumps(params),
    'data': json.dumps(data),
    'cookies': json.dumps(cookies),
    'json': json.dumps(payload),
    'proxy_': json.dumps(proxy_)
}
yield scrapy.Request(url=url, headers=headers, meta=meta_data)
```

And you also need to enable `RequestsDownloaderMiddleware` in `DOWNLOADER_MIDDLEWARES`:

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy_requests_manipulate.downloaderMiddleware.RequestsDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': None,
}
```