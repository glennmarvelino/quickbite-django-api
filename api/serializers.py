from rest_framework import serializers

class MenuSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    restaurant_name = serializers.CharField(max_length=100)
    menu_name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=50)
    price = serializers.FloatField()
    spicy_level = serializers.IntegerField()
    is_available = serializers.BooleanField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(required=False)