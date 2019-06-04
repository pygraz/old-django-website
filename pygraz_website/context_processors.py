from django.conf import settings


def disqus(request):
    """
    Adds the disqus settings to the context.
    """
    return {'disqus': settings.DISQUS_SETTINGS}


def googlemaps(request):
    """
    Adds the Google Maps API key to the context.
    """
    return {'GOOGLEMAPS_API_KEY': settings.GOOGLEMAPS_API_KEY}
