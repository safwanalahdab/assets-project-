from rest_framework import serializers
from inventory.models import Asset


class AssetCreateUpdateModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ["name", "serial_number", "purchase_date", "category", "assigned_to"]


class AssetModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = [
            "id",
            "name",
            "serial_number",
            "purchase_date",
            "category",
            "assigned_to",
        ]
