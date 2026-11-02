from rest_framework import serializers
from tickets.models import Ticket

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

        if "priority" in attrs : 
            raise serializers.ValidationError("لا يمكنك ارسال حقل الاولوية")
        if "status" in attrs : 
            raise serializers.ValidationError("لا يمكنك ارسال حقل الحالة ")
        if "assigned_to" in attrs : 
            raise serializers.ValidationError("لا يمكنك تكليف احد بالمهمة ")

        user = self.context["request"].user 
        asset = attrs.get("related_asset") 

        if asset and not user.profile.is_it_staff and user.id != asset.assigned_assets.id :
            raise serializers.ValidationError("الاصل غير مخصص لهذا الشخص ")





 
