from scrapy.http import Request
from scrapy.utils.request import RequestFingerprinter


class RequestWithFragmentFingerprinter(RequestFingerprinter):
    def fingerprint(self, request: Request) -> bytes:
        return self._fingerprint(request, keep_fragments=True)
