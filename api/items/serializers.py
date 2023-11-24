from rest_framework import serializers

from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "description", "price", "created_at", "updated_at")


class ItemFormSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=225, required=False, help_text="Name of the item"
    )
    description = serializers.CharField(
        max_length=225, required=False, help_text="Item description"
    )
    price = serializers.FloatField(required=False, help_text="Price of the item")

    def create(self, validated_data):
        instance = Item.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_date):
        _ = Item.objects.filter(id=instance.id).update(**validated_date)
        return instance

    def validate(self, attrs):
        if attrs.get("price", None) is not None and attrs["price"] < 0:
            raise ValueError("Price must be positive number")
        return attrs
