from starlette.staticfiles import StaticFiles


# Stolen from https://github.com/lexxai/goit_python_web_hw_14/blob/a4e247e2b1afb57f2d8eb9e63a34d34f4f3e6bd6/hw14/main.py#L99
class CacheControlStaticFiles(StaticFiles):
    def __init__(self, *args, cache_control="no-store", **kwargs):
        self.cache_control = cache_control
        super().__init__(*args, **kwargs)

    def file_response(self, *args, **kwargs):
        resp = super().file_response(*args, **kwargs)
        resp.headers.setdefault("Cache-Control", self.cache_control)
        return resp
