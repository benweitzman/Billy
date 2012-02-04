from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http import HttpResponseRedirect

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Billy.views.home', name='home'),
    # url(r'^Billy/', include('Billy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','Billy.views.index'),
    url(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/images/favicon.ico'}),
    url(r'^debts/$','debt.views.index'),
    url(r'^weekly/$','Billy.views.weekly'),
    url(r'^weekly/redeem/(?P<id>\d+)$/','Billy.views.redeem'),
    url(r'^announcements/$','announcement.views.index'),
    url(r'^announcements/send/(?P<id>\d+)$','announcement.views.send'),
    url(r'^debts/remove/(?P<id>\d+)$','debt.views.removeDebt'),
    url(r'^debts/settle/(?P<id1>\d+)/(?P<id2>\d+)/$','debt.views.settleDebt'),
    url(r'^ajax/getmemos/','Billy.views.getMemos'),
    url(r'^accounts/update','Billy.views.update'),
    url(r'^accounts/profile',lambda x:HttpResponseRedirect("/")),
    url(r'^accounts/',include('invitation.urls')),
    url(r'^accounts/', include('registration.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root':settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root':settings.MEDIA_ROOT}),

)
