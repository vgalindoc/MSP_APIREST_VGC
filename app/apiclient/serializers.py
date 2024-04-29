"""
Serializers for client APIs
"""
from rest_framework import serializers
 
from core.models import Cliente
 
class apiClientSerializer(serializers.ModelSerializer):
    """Serializer for clients."""     
    class Meta:
        model = Cliente
        fields = [
            'id', 'nombre', 'email', 'telefono',
        ]
        read_only_fields = ['id']
     
    def create(self, validated_data):
        """Create a client."""        
        recipe = Cliente.objects.create(**validated_data)         
        return recipe
 
    def update(self, instance, validated_data):
        """Update client."""                                
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
 
        instance.save()
        return instance
    
 
 
class apiClientDetailSerializer(apiClientSerializer):
    """Serializer for client detail view."""
 
    class Meta(apiClientSerializer.Meta):
        fields = apiClientSerializer.Meta.fields 
