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

class BreadForm(forms.ModelForm):
    class Meta:
        model = Bread
        fields = ('flavor',)
        widgets = {
            'type': forms.RadioSelect(),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

