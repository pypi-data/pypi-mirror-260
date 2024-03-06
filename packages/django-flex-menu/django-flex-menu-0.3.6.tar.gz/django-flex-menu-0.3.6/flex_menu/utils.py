from django.urls import get_resolver, URLPattern, URLResolver


def get_project_urls():
    def getter(urls, patterns=None, namespaces=None):
        patterns = [] if patterns is None else patterns
        namespaces = [] if namespaces is None else namespaces

        if not urls:
            return
        l = urls[0]
        if isinstance(l, URLPattern):
            yield patterns + [str(l.pattern)], namespaces + [l.name], l.callback
        elif isinstance(l, URLResolver):
            yield from getter(
                l.url_patterns, patterns + [str(l.pattern)], namespaces + [l.namespace]
            )
        yield from getter(urls[1:], patterns, namespaces)

    for pattern in getter(get_resolver().url_patterns):
        url, names, view = pattern
        names = [n for n in names if n is not None]
        if all(names):
            yield {
                "names": names,
                "view_name": ":".join(names),
                "url": "".join(url),
                "view": view,
            }
            
            
def get_url_choices():
    seen = set()
    for u in sorted(get_project_urls(), key=lambda u: u["view_name"]):
        if (name := u["view_name"]) and name not in seen:
            seen.add(name)
            yield (name, f'{name} ({u["url"]})')
            