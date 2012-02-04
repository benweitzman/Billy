from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from re import compile
from sms.models import Carrier, ContentType, ContentTypePhoneNumber

EXEMPT_URLS = [compile(settings.UPDATE_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class ForceUpdateMiddleware:
    def process_request(self,request):
        u = request.user
        if request.user.is_authenticated():
            if u.first_name == u'' or len(ContentTypePhoneNumber.objects.filter(object_id=u.id)) == 0:
                path = request.path_info.lstrip('/')
                if not any(m.match(path) for m in EXEMPT_URLS):
                    return HttpResponseRedirect(settings.UPDATE_URL)
  