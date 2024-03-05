# starlette\_static\_cache\_control

A `starlette.staticfiles.StaticFiles` subclass allowing custom `Cache-Control`. Just import it (it's called `CacheControlStaticFiles`) and use it as regular `StaticFiles`, it only has an additional `cache_control` argument. The class was stolen from https://github.com/lexxai/goit_python_web_hw_14/blob/a4e247e2b1afb57f2d8eb9e63a34d34f4f3e6bd6/hw14/main.py#L99
