from rest_framework import serializers

from stage_history.models import StageHistory


class StageHistoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageHistory
        fields = "__all__"
