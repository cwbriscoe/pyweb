import os
from webob import Response
from pyramid.view import view_config


@view_config(route_name='favicon', http_cache=3600)
def favicon_view(request):
    here = os.path.dirname(__file__)
    icon = open(os.path.join(here, 'static', 'favicon.ico'))
    return Response(content_type='image/x-icon', app_iter=icon)
