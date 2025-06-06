from django.db import transaction
from rest_framework import serializers

from account.serializers import AccountDetailSerializer
from campaign.serializers import CampaignDetailSerializer
from common.serializers import BaseDetailSerializer, BaseSerializer
from contact.serializers import ContactDetailSerializer
from deal.serializers import DealDetailSerializer
from lead.serializers import LeadDetailSerializer
from meeting.models import Meeting, MeetingParticipant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingParticipant
        fields = ("user", "contact", "lead")


class MeetingSerializer(BaseSerializer):
    participants = ParticipantSerializer(write_only=True, many=True)

    class Meta:
        model = Meeting
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        super().create(validated_data)
        participants = validated_data.pop("participants")
        meeting = Meeting.objects.create(**validated_data)

        # bulk create meeting participants
        meeting_participants = []
        for participant in participants:
            meeting_participants.append(
                MeetingParticipant(
                    meeting=meeting,
                    user=participant["user"],
                    contact=participant["contact"],
                    lead=participant["lead"],
                )
            )
        MeetingParticipant.objects.bulk_create(meeting_participants)

        return meeting

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        participants = validated_data.pop("participants")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        MeetingParticipant.objects.filter(meeting=instance).delete()

        # bulk create meeting participants
        meeting_participants = []
        for participant in participants:
            meeting_participants.append(
                MeetingParticipant(
                    meeting=instance,
                    user=participant["user"],
                    contact=participant["contact"],
                    lead=participant["lead"],
                )
            )
        MeetingParticipant.objects.bulk_create(meeting_participants)

        return instance


class MeetingDetailSerializer(BaseDetailSerializer):
    participants = serializers.SerializerMethodField()
    related_deal = DealDetailSerializer(read_only=True)
    related_lead = LeadDetailSerializer(read_only=True)
    related_account = AccountDetailSerializer(read_only=True)
    related_campaign = CampaignDetailSerializer(read_only=True)
    related_contact = ContactDetailSerializer(read_only=True)

    class Meta:
        model = Meeting
        fields = "__all__"

    def get_participants(self, obj):
        participants = MeetingParticipant.objects.filter(meeting=obj)
        result = []

        for participant in participants:
            user = participant.user or participant.lead or participant.contact
            if user:
                result.append({"name": user.full_name, "email": user.email})

        return result
