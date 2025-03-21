from rest_framework import serializers

from authentication.serializers import UserSerializer
from common.serializers import BaseDetailSerializer, BaseSerializer
from contact.models import Contact


class ContactSerializer(BaseSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

    def validate_email(self, value):
        contact_id = self.instance.id if self.instance else None
        if Contact.objects.filter(email=value).exclude(id=contact_id).exists():
            raise serializers.ValidationError("This email is used by another contact")
        return value

    def create(self, validated_data):
        super().create(validated_data)
        contact = Contact.objects.create(**validated_data)
        return contact

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ContactDetailSerializer(BaseDetailSerializer, serializers.ModelSerializer):
    from lead.serializers import LeadSourceSerializer

    contact_owner = UserSerializer(read_only=True)
    lead_source = LeadSourceSerializer(read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"
