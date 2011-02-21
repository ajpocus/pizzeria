import datetime
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import list_detail
from order.models import Customer, Order, Pizza, Bread, PizzaForm, BreadForm

def place_order(request):
    c = Customer.objects.create()
    o = Order.objects.create(customer=c, date=datetime.datetime.now())
    order_id = o.id
    url = "/order/pizza/" + str(order_id)
    return redirect(url)

def order_pizza(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
	form = PizzaForm(request.POST)
	if form.is_valid():
	    data = form.cleaned_data
	    size = str(data['size'])
	    crust = str(data['crust'])
	    toppings = data['toppings']

	    pizza = Pizza.objects.create(size=size, crust=crust)
	    for topping in toppings:
		pizza.toppings.add(topping)

	    order.pizzas.add(pizza)
	    url = '/order/pizza/' + str(order_id)
	    redirect(url)
    else:
	form = PizzaForm()

    return list_detail.object_list(
	request,
	queryset = Order.objects.filter(id=order_id),
	template_name = "order/pizza.html",
	template_object_name = "order",
	extra_context = {
	    "form": form,
	    "order": order,
	},
    )

def order_bread(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = BreadForm(request.POST)
        if form.is_valid():
	    data = form.cleaned_data
	    type = str(data['type'])
	    bread = Bread.objects.create(type=type)
	    order.breads.add(bread)
	    url = '/order/bread/' + str(order_id)
	    redirect(url)
    else:
	form = BreadForm()

    return list_detail.object_list(
	request,
	queryset = Order.objects.filter(id=order_id),
	template_name = "order/bread.html",
	template_object_name = "order",
	extra_context = {
	    "form": form,
	    "order": order,
	}
    )
