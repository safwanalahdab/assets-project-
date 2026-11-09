from rest_framework import serializers
from tickets.models import Ticket
from .permissions import is_staff


class TicketCreateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
            "related_asset",
            "tags",
            "status",
            "assigned_to",
        ]

    def validate(self, attrs):

        if "priority" in attrs:
            raise serializers.ValidationError("لا يمكنك ارسال حقل الاولوية")
        if "status" in attrs:
            raise serializers.ValidationError("لا يمكنك ارسال حقل الحالة ")
        if "assigned_to" in attrs:
            raise serializers.ValidationError("لا يمكنك تكليف احد بالمهمة ")

        user = self.context["request"].user
        asset = attrs.get("related_asset")

        if asset and not is_staff(user) and user.id != asset.assigned_assets.id:
            raise serializers.ValidationError("الاصل غير مخصص لهذا الشخص ")


class TicketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "creator",
            "related_asset",
            "tags",
            "status",
            "assigned_to",
            "created_at",
            "updated_at",
        ]


class TicketStatusFilterInputSerializer(serializers.Serializer):
    status = serializers.CharField(choices=Ticket.status.choices, required=False)


class TicketUpdateInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
            "related_asset",
            "tags",
            "status",
            "assigned_to",
        ]

    def validate(self, attrs):
        user = self.context['request'].user 

        if not is_staff(user) : 
            if "priority" or "related_asset" or "assigned_to" in attrs : 
                raise serializers.ValidationError("لا يمكنك تعديل هذه الحقول") 


