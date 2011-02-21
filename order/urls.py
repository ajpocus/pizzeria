from django.conf.urls.defaults import *
from order.views import order_pizza, order_bread

urlpatterns = patterns('order.views',
    url(r'^$', 'place_order'),
    url(r'pizza/(?P<order_id>\d+)$', order_pizza),
    url(r'bread/(?P<order_id>\d+)$', order_bread),
)

