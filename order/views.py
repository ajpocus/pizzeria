import datetime
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.generic import list_detail
from order.models import Customer, Order, Pizza, Bread
from order.forms import PizzaForm, BreadForm, CustomerForm

def place_order(request):
    c = Customer.objects.create()
    o = Order.objects.create(customer=c, date=datetime.datetime.now())
    order_id = o.id
    url = "/order/pizza/" + str(order_id)
    return redirect(url)

def order_pizza(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
	if 'pizza' in request.POST and request.POST['pizza'] == 'Update':
	    pizza_form = PizzaForm(request.POST)
	    if pizza_form.is_valid():
		data = pizza_form.cleaned_data
		size = str(data['size'])
		crust = str(data['crust'])
		toppings = data['toppings']

		pizza = Pizza.objects.create(size=size, crust=crust)
		for topping in toppings:
		    pizza.toppings.add(topping)

		order.pizzas.add(pizza)
		order.save()
		url = '/order/pizza/' + str(order_id)
		return redirect(url)
	    
	else:
	    pizza_form = PizzaForm()

	if 'customer' in request.POST and request.POST['customer'] == 'Update':
	    customer_form = CustomerForm(request.POST)
	    if customer_form.is_valid():
		data = customer_form.cleaned_data
		name = str(data['name'])
		number = str(data['number'])
		customer = Customer.objects.create(name=name, number=number)
		order.customer = customer
		order.save()
		url = '/order/pizza/' + str(order_id)
		return redirect(url)	
        else:
	    customer_form = CustomerForm()
    else:
	pizza_form = PizzaForm()
	customer_form = CustomerForm()

    return list_detail.object_list(
	request,
	queryset = Order.objects.filter(id=order_id),
	template_name = "order/pizza.html",
	template_object_name = "order",
	extra_context = {
	    "pizza_form": pizza_form,
	    "customer_form": customer_form,
	    "order": order,
	},
    )

def order_bread(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        if 'bread' in request.POST and request.POST['bread'] == 'Update':
	    bread_form = BreadForm(request.POST)
	    if bread_form.is_valid():
		data = bread_form.cleaned_data
		type = str(data['type'])
		bread = Bread.objects.create(type=type)
		order.breads.add(bread)
		url = '/order/bread/' + str(order_id)
		return redirect(url)
	else:
	    bread_form = BreadForm()

	if 'customer' in request.POST and request.POST['customer'] == 'Update':
            customer_form = CustomerForm(request.POST)
            if customer_form.is_valid():
                data = customer_form.cleaned_data
                name = str(data['name'])
                number = str(data['number'])
                customer = Customer.objects.create(name=name, number=number)
                order.customer = customer
                order.save()
                url = '/order/pizza/' + str(order_id)
                return redirect(url)
        else:
            customer_form = CustomerForm()

    else:
	bread_form = BreadForm()
	customer_form = CustomerForm()

    return list_detail.object_list(
	request,
	queryset = Order.objects.filter(id=order_id),
	template_name = "order/bread.html",
	template_object_name = "order",
	extra_context = {
	    "bread_form": bread_form,
	    "customer_form": customer_form,
	    "order": order,
	}
    )

