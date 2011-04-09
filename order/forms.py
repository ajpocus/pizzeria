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
        size = str(data['size'])
        crust = str(data['crust'])
        toppings = data['toppings']

        pizza = Pizza.objects.create(size=size, crust=crust)
        for topping in toppings:
	    pizza.toppings.add(topping)

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
	data = bread_form.cleaned_data
        flavor = str(data['flavor'])
        bread = Bread.objects.create(flavor=flavor)
        order.breads.add(bread)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

    def process(self, order):
	data = customer_form.cleaned_data
        name = str(data['name'])
        number = str(data['number'])
        customer = Customer.objects.create(name=name, number=number)
        order.customer = customer
        order.save()

