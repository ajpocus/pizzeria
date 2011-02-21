from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pizzeria/', include('pizzeria.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^order/', include('order.urls')),
    (r'^line/', include('line.urls')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
	{'document_root': settings.MEDIA_ROOT}),
)
