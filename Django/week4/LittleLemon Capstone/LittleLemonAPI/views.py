from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import MenuItemsSerializer, UserSerializer
from .models import MenuItem
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from django.http import Http404

class IsManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            return request.user.groups.filter(name='manager').exists()
        return False

class IsManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='manager').exists():
            return True
        return False

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemsSerializer
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


class ManagerUserGroupView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOnly]
    def get_queryset(self):
        try:
            group = Group.objects.get(name='manager')
        except Group.DoesNotExist:
            raise Http404("Group does not exist.")
        return User.objects.filter(groups=group)

    def create(self, requset):
        serializer = self.get_serializer(data=requset.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DeliveryCrewUserGroupView(generics.ListCreateAPIView):
    # def update(self, requset, id):
    #     user = User.objects.get(pk=id)
    #     serializer = UserSerializer(user, data=requset.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsManagerOnly]
    def get_queryset(self):
        try:
            group = Group.objects.get(name='delivery-crew')
        except Group.DoesNotExist:
            raise Http404("Group does not exist.")
        return User.objects.filter(groups=group)