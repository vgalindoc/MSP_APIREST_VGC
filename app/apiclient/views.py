from django.shortcuts import render

# Create your views here.
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
 
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
 
from core.models import (
    Cliente,    
)
 
from apiclient import serializers
 
class apiclientViewSet(viewsets.ModelViewSet):
 
    serializer_class = serializers.apiClientDetailSerializer
    queryset = Cliente.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        """Retrieve clients for authenticated user."""        
        queryset = self.queryset        
        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.apiClientSerializer        
        return self.serializer_class
   
    def perform_create(self, serializer):
        """Create a new client."""
        serializer.save(user=self.request.user)
        
 # Class base Client
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
   
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
        """Filter queryset to authenticated user."""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(cliente__isnull=False)
 
        return queryset.filter(
            user=self.request.user
        ).order_by('-name').distinct()
 