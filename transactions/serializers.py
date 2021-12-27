import json

from rest_framework import serializers
from .models import TransactionHistory


class TransactionHistorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = TransactionHistory
        fields = (
            "name",
            "canonical_date",
            "timestamp",
            "transaction_count"
        )
        read_only_fields = fields