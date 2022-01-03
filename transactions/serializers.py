import json

from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    transaction_avg = serializers.SerializerMethodField("get_transaction_avg")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_transaction_avg(self, obj):
        try:
            return obj['transaction_avg']
        except:
            return None
    class Meta:
        model = TransactionHistory
        fields = (
            "eatery_id",
            "canonical_date",
            "block_end_time",
            "transaction_avg"
        )
        read_only_fields = fields