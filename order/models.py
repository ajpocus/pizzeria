import decimal
from decimal import Decimal
from django.db import models

quant = Decimal('0.01')

class Flavor(models.Model):
    name = models.CharField(max_length=24)
    base_price = models.DecimalField(max_digits=4,
		    decimal_places=2,
		    default=3.99)

    def __unicode__(self):
	return self.name

class Size(models.Model):
    name = models.CharField(max_length=24)
    base_price = models.DecimalField(max_digits=4,
		    decimal_places=2,
		    default=0.00)

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
    size = models.ForeignKey(Size, null=True)
    toppings = models.ManyToManyField(Topping, null=True)
    crust = models.ForeignKey(Flavor, null=True)
    base_price = models.DecimalField(max_digits=4, 
				    decimal_places=2, 
				    default=5.00)

    def save(self, *args, **kwargs):
	if not Pizza.objects.filter(id=self.id):
	    super(Pizza, self).save(*args, **kwargs)
	else:
	    price = Decimal('0.00')
	    if self.size:
		price = self.size.base_price
	    for topping in self.toppings.all():
		if topping.base_price:
		    price = price + topping.base_price

	    self.base_price = decimal.Decimal(str(price)).quantize(quant)
	    super(Pizza, self).save(*args, **kwargs)

    def __unicode__(self):
	if self.size.name:
	    name = self.size.name + " Pizza"
	else:
	    name = "Pizza"
	for topping in self.toppings.all():
	    if topping.name:
		name = name + ", " + topping.name
	return name

class Bread(models.Model):
    flavor = models.ForeignKey(Flavor)
    base_price = models.DecimalField(max_digits=4,
				    decimal_places=2,
				    default=4.00)

    def save(self, *args, **kwargs):
	self.base_price = Decimal(self.flavor.base_price).quantize(quant)
	super(Bread, self).save(*args, **kwargs)

    def __unicode__(self):
	return self.type

class Customer(models.Model):
    name = models.CharField(max_length=64)
    number = models.CharField(max_length=20)

    def __unicode__(self):
	return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer)
    date = models.DateField()
    pizzas = models.ManyToManyField(Pizza, blank=True)
    breads = models.ManyToManyField(Bread, blank=True)
    is_made = models.BooleanField(default=False)
    subtotal = models.DecimalField(max_digits=6, 
				decimal_places=2,
				default=0.00)
    tax = models.DecimalField(max_digits=6,
			    decimal_places=2,
			    default=0.00)
    total = models.DecimalField(max_digits=6, 
				decimal_places=2, 
				default=0.00)

    def save(self, *args, **kwargs):
	if not Order.objects.filter(id=self.id):
	    super(Order, self).save(*args, **kwargs)
	else:
	    decimal.getcontext().rounding = decimal.ROUND_HALF_EVEN
	    self.subtotal = Decimal('0.00')

	    for pizza in self.pizzas.all():
		self.subtotal += pizza.base_price
		for topping in pizza.toppings.all():
		    self.subtotal += topping.base_price

	    for bread in self.breads.all():
		self.subtotal += bread.base_price

	    self.tax = Decimal('0.06') * self.subtotal
	    self.total = self.subtotal + self.tax
	    self.subtotal = self.subtotal.quantize(quant)
	    self.tax = self.tax.quantize(quant)
	    self.total = self.total.quantize(quant)
	    super(Order, self).save(*args, **kwargs)

    def __unicode__(self):
	return str(self.id)

