from django.db import models

# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    # null=True, related_name='+' means that the reverse relationship is not required
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')


class Product(models.Model):
    # max_length is the maximum number of characters in the field
    title = models.CharField(max_length=255)
    # blank=True means that the field is optional
    description = models.TextField(blank=True)
    # max_digits is the maximum number of digits in the field, decimal_places is the number of decimal places
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # default=0 means that the field will be set to 0 by default
    inventory = models.IntegerField(default=0)
    # auto_now=True means that the field will be set to the current date and time whenever the model is saved
    last_update = models.DateTimeField(auto_now=True)
    # on_delete=models.PROTECT means that the product will not be deleted if the collection is deleted
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(
        Promotion, blank=True)  # blank=True means that the field is optional.
    # ManyToManyField means that there can be many products in a collection, and there can be many collections in a product.


class Customer(models.Model):

    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')]

    # max_length is the maximum number of characters in the field
    first_name = models.CharField(max_length=255)
    # max_length is the maximum number of characters in the field
    last_name = models.CharField(max_length=255)
    # unique=True means that the field must be unique
    email = models.EmailField(max_length=255, unique=True)
    # max_length is the maximum number of characters in the field
    phone = models.CharField(max_length=255)
    # null=True means that the field is optional
    birth_date = models.DateField(null=True)
    # default=MEMBERSHIP_BRONZE means that the field will be set to MEMBERSHIP_BRONZE by default
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)


class Order(models.Model):

    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')]

    # auto_now_add=True means that the field will be set to the current date and time whenever the model is saved
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)  # default=PAYMENT_STATUS_PENDING means that the field will be set to PAYMENT_STATUS_PENDING by default
    # on_delete=models.PROTECT means that the order will not be deleted if the customer is deleted
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # on_delete=models.PROTECT means that the order item will not be deleted if the order is deleted
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    # on_delete=models.PROTECT means that the order item will not be deleted if the product is deleted
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    # PositiveSmallIntegerField means that the field will be set to a positive integer
    quantity = models.PositiveSmallIntegerField()
    # max_digits is the maximum number of digits in the field, decimal_places is the number of decimal places
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    # max_length is the maximum number of characters in the field
    street = models.CharField(max_length=255)
    # max_length is the maximum number of characters in the field
    city = models.CharField(max_length=255)
    # on_delete=models.CASCADE means that the customer will be deleted whenever the address is deleted
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Cart(models.Model):
    # auto_now_add=True means that the field will be set to the current date and time whenever the model is saved
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    # on_delete=models.CASCADE means that the cart item will be deleted whenever the cart is deleted
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # on_delete=models.CASCADE means that the cart item will be deleted whenever the product is deleted
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # PositiveSmallIntegerField means that the field will be set to a positive integer
    quantity = models.PositiveSmallIntegerField()
