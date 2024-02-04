from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Order, OrderItem, DailyData
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, DailyDataSerializer
from accounts.permissions import IsAccountType, IsBuyer, IsSeller

# class ProductListAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAccountType]
#     allowed_roles = ['SELLER']
class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        elif self.request.method == 'POST':
            return [IsAccountType(allowed_roles=['SELLER'])]
        return super(ProductListAPIView, self).get_permissions()

class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartListAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAccountType]
    allowed_roles = ['BUYER']


class CartDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAccountType]
    allowed_roles = ['BUYER']

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class CartItemCreateAPIView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAccountType]
    allowed_roles = ['BUYER']


class OrderListAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAccountType]
    allowed_roles = ['BUYER']

    def perform_create(self, serializer):
        # Clear or mark cart items as ordered when creating an order
        cart_items = self.request.user.cart_items.all()
        for cart_item in cart_items:
            # Perform any logic needed for marking as ordered or clearing the cart
            cart_item.delete()

        serializer.save(user=self.request.user)
    

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAccountType]
    allowed_roles = ['BUYER']

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    
class DailyDataListAPIView(generics.ListCreateAPIView):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer

class DailyDataDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyData.objects.all()
    serializer_class = DailyDataSerializer
