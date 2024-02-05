from django.db import models
from accounts.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    items = models.ManyToManyField('CartItem', related_name='cart_items')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.CharField(max_length=255)
    order_status = models.CharField(choices=[
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled')
    ], max_length=20)
    payment_method = models.CharField(choices=[
        ('CREDIT_CARD', 'Credit Card'),
        ('DEBIT_CARD', 'Debit Card'),
        ('WALLET', 'Wallet')
    ], max_length=20)
    order_items = models.ManyToManyField('CartItem', through='OrderItem', related_name='orders_items')

@receiver(post_save, sender=Order)
def empty_cart(sender, instance, created, **kwargs):
    if created:
        instance.user.cart.items.clear()
        instance.user.cart.delete()




class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=CASCADE, related_name='items')
    cart_item = models.ForeignKey(CartItem, on_delete=CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class DailyData(models.Model):
    date = models.DateField(primary_key=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)