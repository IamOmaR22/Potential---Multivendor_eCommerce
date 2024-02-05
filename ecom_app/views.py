from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Product, Cart, CartItem, Order, OrderItem, DailyData
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, OrderSerializer, DailyDataSerializer, OrderItemSerializer
from accounts.permissions import IsAccountType, IsBuyer, IsSeller
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# class ProductListAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get_permissions(self):
#         if self.request.method == 'GET':
#             return [permissions.AllowAny()]
#         elif self.request.method == 'POST':
#             return [IsAccountType(allowed_roles=['SELLER'])]
#         return super(ProductListAPIView, self).get_permissions()
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAccountType]
    allowed_roles = ['SELLER']

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAccountType]
    # allowed_roles = ['SELLER']
    

# Template view
class ProductListTemplateView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    template_name = 'product_list.html'

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.request.GET.get('page', 1)
        paginator = Paginator(queryset, 15)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        serializer = self.get_serializer(products, many=True)

        return render(request, self.template_name, {'products': serializer.data})

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
        user = self.request.user
        existing_cart = Cart.objects.filter(user=user).first()

        if existing_cart:
            existing_cart.updated_at = timezone.now()
            existing_cart.save()
            serializer.instance = existing_cart
        else:
            serializer.save(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        user = self.request.user

        try:
            cart = user.cart
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

        product_id = self.request.data.get('product')
        quantity = self.request.data.get('quantity', 1)

        product = Product.objects.get(pk=product_id)
        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        cart.items.add(cart_item)
        serializer.instance = cart_item
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        if not queryset.exists():
            return Response({"detail": "No orders available."}, status=status.HTTP_200_OK)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user

        try:
            cart = user.cart
        except ObjectDoesNotExist:
            return Response({"detail": "User has no cart."},
                            status=status.HTTP_400_BAD_REQUEST)

        if cart.items.count() == 0:
            return Response({"detail": "Cart is empty. Add items to the cart before creating an order."},
                            status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save(user=user)
        order_items_data = self.request.data.get('order_items', [])

        created_order_items = []
        for order_item_data in order_items_data:
            cart_item_id = order_item_data.get('cart_item')
            quantity = order_item_data.get('quantity', 1)

            try:
                cart_item = CartItem.objects.get(pk=cart_item_id)
                order_item = OrderItem.objects.create(order=order, cart_item=cart_item, quantity=quantity)
                created_order_items.append(order_item)
            except CartItem.DoesNotExist:
                return Response({"detail": f"CartItem with id {cart_item_id} does not exist."},
                                status=status.HTTP_400_BAD_REQUEST)

        order_items_serializer = OrderItemSerializer(created_order_items, many=True)

        return Response({
            "detail": "Order created successfully",
            "order_id": order.id,
            "order_items": order_items_serializer.data,
        }, status=status.HTTP_201_CREATED)

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
