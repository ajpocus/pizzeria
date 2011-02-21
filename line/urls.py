from django.conf.urls.defaults import *
from line.views import view_orders

urlpatterns = patterns('line.views',
    url(r'^$', view_orders),
)

