from django.conf import settings


def disqus(request):
    """
    Adds the disqus settings to the context.
    """
    return {'disqus': settings.DISQUS_SETTINGS}
