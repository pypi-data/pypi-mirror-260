from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

def uncompress_string(c):
    from io import BytesIO
    from gzip import GzipFile
    zbuf = BytesIO(c)
    with GzipFile(mode='rb', compresslevel=6, fileobj=zbuf) as zfile:
        return zfile.read()

class ForceDebugToolbarMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """Add html, head, and body tags so debug toolbar will activate."""
        if not (request.GET.get('debug') and settings.DEBUG):
            return response

        content = response.content
        was_compressed = False
        if 'content-encoding' in response:
            if response['Content-Encoding'] != 'gzip':
                logger.warning("Unsure how to debug response on content encoding {0}".format(response['Content-Encoding']))
                return response
            content = uncompress_string(response.content)
            was_compressed = True

        if b'<body>' not in content:
            response.content = '<html><head></head><body>%s</body></html>' % content
            response['Content-Length'] = str(len(response.content))
            response['Content-Type'] = 'text/html'

            if was_compressed:
                del response['Content-Encoding']
                if response.has_header('ETag'):
                    response['ETag'] = re.sub('"$', ';ungzip"', response['ETag'])

        return response
