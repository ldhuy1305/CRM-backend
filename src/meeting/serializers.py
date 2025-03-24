from django.db import transaction
from rest_framework import serializers

from common.serializers import BaseDetailSerializer, BaseSerializer
from meeting.models import Meeting, MeetingParticipant


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingParticipant
        fields = ('user', 'contact', 'lead')


class MeetingSerializer(BaseSerializer):
    participants = ParticipantSerializer(write_only=True, many=True)

    class Meta:
        model = Meeting
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        super().create(validated_data)
        participants = validated_data.pop('participants')
        meeting = Meeting.objects.create(**validated_data)

        # bulk create meeting participants
        meeting_participants = []
        for participant in participants:
            meeting_participants.append(
                MeetingParticipant(
                    meeting=meeting,
                    user=participant['user'],
                    contact=participant['contact'],
                    lead=participant['lead'],
                )
            )
        MeetingParticipant.objects.bulk_create(meeting_participants)
        
        return meeting

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class MeetingDetailSerializer(BaseDetailSerializer, serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"
