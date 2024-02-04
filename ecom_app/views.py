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

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemListAPIView(generics.ListAPIView):
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
        order_items_data = self.request.data.pop('order_items', [])

        order = serializer.save(user=self.request.user)

        for order_item_data in order_items_data:
            cart_item_id = order_item_data.get('cart_item')
            quantity = order_item_data.get('quantity', 1)
            
            OrderItem.objects.create(order=order, cart_item_id=cart_item_id, quantity=quantity)

        return Response({"detail": "Order created successfully"}, status=status.HTTP_201_CREATED)
    

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
