from django.views.generic import list_detail
from order.models import Order

def view_orders(request):
    return list_detail.object_list(
	request,
	queryset = Order.objects.filter(is_made=False),
	template_name = "line/view_orders.html",
	template_object_name = "order",
	)

