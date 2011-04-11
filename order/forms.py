from django import forms
from order.models import Pizza, Bread, Customer

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('size', 'toppings', 'crust')
        widgets = {
	    'size': forms.RadioSelect(),
            'crust': forms.RadioSelect(),
            'toppings': forms.CheckboxSelectMultiple(),
        }

    def process(self, order):
	data = self.cleaned_data
        size = data['size']
        crust = data['crust']
        toppings = data['toppings']

        pizza = Pizza.objects.create()
	pizza.size = size
	pizza.crust = crust
        for topping in toppings:
	    pizza.toppings.add(topping)
	pizza.save()

        order.pizzas.add(pizza)
        order.save()

class BreadForm(forms.ModelForm):
    class Meta:
        model = Bread
        fields = ('flavor',)
        widgets = {
            'type': forms.RadioSelect(),
        }

    def process(self, order):
	data = self.cleaned_data
        flavor = data['flavor']
        bread = Bread.objects.create(flavor=flavor)
        order.breads.add(bread)
	order.save()

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

    def process(self, order):
	data = self.cleaned_data
        name = str(data['name'])
        number = str(data['number'])
        customer = Customer.objects.create(name=name, number=number)
        order.customer = customer
        order.save()

