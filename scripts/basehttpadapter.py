import requests.adapters


class BaseHTTPAdapter(requests.adapters.HTTPAdapter):
    def close(self):
        super().close()
        if hasattr(self, 'pools'):
            self.pools.clear()
    def get_connection_with_tls_context(self, request, verify, proxies=None, cert=None):
        return self.get_connection(request.url, proxies)
