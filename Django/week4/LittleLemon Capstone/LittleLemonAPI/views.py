from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import MenuItemsSerializer
from .models import MenuItem
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the request method is safe (GET, HEAD, OPTIONS)
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.groups.filter(name='Manager').exists()
        return False
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    # def list(self, request):
    #     queryset = self.get_queryset()
    #     seializer = MenuItemsSerializer(queryset, many=True)
    #     return Response(seializer.data)
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
    permission_classes = [IsAuthenticated, IsManagerOrReadOnly]
