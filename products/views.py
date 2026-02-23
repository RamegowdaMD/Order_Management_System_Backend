from rest_framework import generics, permissions
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Product
from rest_framework.views import APIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from asgiref.sync import async_to_sync
from .services import ProductService
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import status


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]

        return [permissions.IsAdminUser()]

    
    @method_decorator(cache_page(60 * 5))  
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    # def get(self, request, pk):
    #     product = async_to_sync(ProductService.get_product)(pk)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)



    def get(self, request, pk):
            try:

                product = async_to_sync(ProductService.get_product)(pk)
                serializer = ProductSerializer(product)
                return Response(serializer.data)

            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )




