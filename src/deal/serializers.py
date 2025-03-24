from rest_framework import serializers

from authentication.serializers import UserSerializer
from common.serializers import BaseDetailSerializer, BaseNameSerializer, BaseSerializer
from contact.serializers import ContactDetailSerializer
from deal.models import Deal, LostReason, Stage
from stage_history.models import StageHistory
from stage_history.serializers import StageHistoryDetailSerializer


class StageDetailSerializer(BaseNameSerializer):
    class Meta:
        model = Stage
        fields = BaseNameSerializer.Meta.fields + ["probability"]


class LostReasonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostReason
        fields = ["id", "reason"]


class DealSerializer(BaseSerializer):
    class Meta:
        model = Deal
        fields = "__all__"

    def create(self, validated_data):
        super().create(validated_data)
        deal = Deal.objects.create(**validated_data)

        # Create stage history
        request = self.context.get("request")
        stage = validated_data.get("stage", None)
        StageHistory.objects.create(
            stage=stage,
            deal=deal,
            amount=deal.amount,
            probability=deal.probability,
            expected_revenue=deal.expected_revenue,
            created_by=request.user,
        )

        return deal

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        # Create stage history
        request = self.context.get("request")
        stage = validated_data.get("stage", None)
        if instance.stage != stage:
            StageHistory.objects.create(
                stage=stage,
                amount=validated_data.get("amount"),
                probability=validated_data.get("probability"),
                expected_revenue=validated_data.get("expected_revenue"),
                deal=instance,
                created_by=request.user,
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DealDetailSerializer(BaseDetailSerializer, serializers.ModelSerializer):
    from account.serializers import AccountDetailSerializer

    deal_owner = UserSerializer(read_only=True)
    account = AccountDetailSerializer(read_only=True)
    contact = ContactDetailSerializer(read_only=True)
    stage = StageDetailSerializer(read_only=True)
    lost_reason = LostReasonDetailSerializer(read_only=True)
    stage_histories = StageHistoryDetailSerializer(
        source="stage_history.all", many=True, read_only=True
    )

    # TODO: serializer of Campaign

    class Meta:
        model = Deal
        fields = "__all__"
