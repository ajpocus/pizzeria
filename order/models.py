from django.db import models
from django.forms import ModelForm, CheckboxSelectMultiple, RadioSelect
from decimal import Decimal

SIZE_CHOICES = (
    ('S', 'Small'), 
    ('M', 'Medium'), 
    ('L', 'Large'), 
    ('XL', 'Extra Large'),
)

CRUST_CHOICES = (
    ('OG', 'Original'), 
    ('GR', 'Garlic'), 
    ('BT', 'Butter'),
)

BREAD_CHOICES = (
    ('GR', 'Garlic'),
    ('CN', 'Cinnamon'),
    ('CJ', 'Cajun'),
)
    
class Customer(models.Model):
    name = models.CharField(max_length=64)
    number = models.CharField(max_length=20)

    def __unicode__(self):
	return self.name


class Topping(models.Model):
    name = models.CharField(max_length=24)
    base_price = models.DecimalField(max_digits=4,
				decimal_places=2,
				default=0.99)

    def __unicode__(self):
	return self.name

class Pizza(models.Model):
    size = models.CharField(max_length=6, choices=SIZE_CHOICES)
    toppings = models.ManyToManyField(Topping, blank=True)
    crust = models.CharField(max_length=8,
			    default='Original',
			    blank=True,
			    choices=CRUST_CHOICES)
    base_price = models.DecimalField(max_digits=4, 
				    decimal_places=2, 
				    default=5.00)

    def save(self, *args, **kwargs):
	if self.size == 'S':
	    self.base_price = Decimal('5.00')
	elif self.size == 'M':
	    self.base_price = Decimal('8.00')
	elif self.size == 'L':
	    self.base_price = Decimal('11.00')
	elif self.size == 'XL':
	    self.base_price = Decimal('14.00')
	else:
	    return ValueError, "Invalid size."
	super(Pizza, self).save(*args, **kwargs)

class Bread(models.Model):
    type = models.CharField(max_length=8, choices=BREAD_CHOICES)
    base_price = models.DecimalField(max_digits=4,
				    decimal_places=2,
				    default=4.00)

    def __unicode__(self):
	return self.type

class Order(models.Model):
    customer = models.ForeignKey(Customer)
    date = models.DateField()
    pizzas = models.ManyToManyField(Pizza, blank=True)
    breads = models.ManyToManyField(Bread, blank=True)
    is_made = models.BooleanField(default=False)
    subtotal = models.DecimalField(max_digits=6, 
				decimal_places=2,
				default=0.00)
    tax = models.IntegerField(default=6)
    total = models.DecimalField(max_digits=6, 
				decimal_places=2, 
				default=0.00)

    def save(self, *args, **kwargs):
	if not Order.objects.filter(id=self.id):
	    super(Order, self).save(*args, **kwargs)
	else:
	    self.subtotal = Decimal('0.00')
	    for pizza in self.pizzas.all():
		self.subtotal += pizza.base_price
		for topping in pizza.toppings.all():
		    self.subtotal += topping.base_price

	    for bread in self.breads.all():
		self.subtotal += bread.base_price

	    self.tax = Decimal('0.06') * self.subtotal
	    self.total = self.subtotal + self.tax
	    super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
	return str(self.id)

class PizzaForm(ModelForm):
    class Meta:
	model = Pizza
	fields = ('size', 'toppings', 'crust')
	widgets = {
	    'toppings': CheckboxSelectMultiple(),	
	}

class BreadForm(ModelForm):
    class Meta:
	model = Bread
	fields = ('type',)
	widgets = {
	    'type': RadioSelect(),
	}


