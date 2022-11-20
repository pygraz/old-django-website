class Registry(object):
    """
    The content registry represents an index of all the model classes that
    are relevant for user content.
    """

    _idx = []

    def register(self, proxy):
        """
        Adds a content proxy to the index.
        """
        self._idx.append(proxy)

    def get_all(self, request, user=None):
        """
        Returns a generator of tuples containing the label, model class and
        queryset provided by each proxy already tailored to the given user.
        """
        for proxy_cls in self._idx:
            yield proxy_cls(request, user)


class BaseProxy(object):
    """
    Every content provider has to register a so-called contentproxy which
    should extend this base class.
    """

    _has_content = None
    label = "Meine Daten"
    model_class = None

    def __init__(self, request, user):
        self.request = request
        self.user = user
        if not hasattr(self, "items_template") or self.item_template is None:
            self.items_template = "accounts/contents/{0}_items.html".format(self.model_class.__name__.lower())

    def get_queryset(self):
        return []

    @property
    def has_content(self):
        if self._has_content is None:
            self._has_content = bool(len(self.items))
        return self._has_content

    @property
    def items(self):
        if not hasattr(self, "_items") or self._items is None:
            self._items = self.get_queryset()
        return self._items


REGISTRY = Registry()


def register(proxy):
    REGISTRY.register(proxy)


def get_all(request, user=None):
    return REGISTRY.get_all(request, user)
