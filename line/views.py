from django.views.generic import list_detail
from django.shortcuts import redirect
from order.models import Order

def view_orders(request):
    if request.method == 'POST':
	if 'Clear' in request.POST:
	    id = request.POST['Clear']
	    order = Order.objects.get(id=id)
	    order.is_made = True
	    order.save()
	    redirect('/line')
	
    return list_detail.object_list(
	request,
	queryset = Order.objects.filter(is_made=False),
	template_name = "line/view_orders.html",
	template_object_name = "order",
	)

