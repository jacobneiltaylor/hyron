from py_mini_racer.py_mini_racer import MiniRacer

from .web import WebPrefixListDatasource


class JsonQueryListDatasource(WebPrefixListDatasource, register="jsonquery"):
    """
        This extension of the WebPrefixListDatasource allows users
        to embed Javascript in their prefix list definitions
        to filter and transform JSON data
    """
    def __init__(self, origin, query):
        self._ctx = self._build_v8_context(query)

        args = {
            "format": "json",
            "origin": origin
        }

        super().__init__(**args)

    @staticmethod
    def _build_v8_context(query) -> MiniRacer:
        js_code = f"let queryfunc = {query}"

        ctx = MiniRacer()
        ctx.eval(js_code)
        return ctx

    def _load_origin(self, origin):
        data = super()._load_origin(origin)
        result = self._ctx.call("queryfunc", data)
        assert(isinstance(result, list))
        return result
