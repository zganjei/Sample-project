from django.conf import settings
from django.urls.base import resolve
from django.urls.exceptions import Resolver404




def default_context(request):
    referrer = ''
    if request.META.get("HTTP_REFERER"):
        referrer = request.META.get("HTTP_REFERER")

    # SITE_URL = settings.SITE_URL
    # STATIC_URL = settings.STATIC_URL
    # SITE_VERSION = settings.SITE_VERSION
    # MEDIA_URL = settings.MEDIA_URL

    try:
        current_url_name = resolve(request.path_info).url_name
    except Resolver404:
        current_url_name = ''

    # return {'referrer': referrer, 'SITE_URL': SITE_URL, 'STATIC_URL': STATIC_URL, 'SITE_VERSION': SITE_VERSION, 'MEDIA_URL': MEDIA_URL,
    #         'current_url_name': current_url_name}

    return {'referrer': referrer, 'current_url_name': current_url_name}
