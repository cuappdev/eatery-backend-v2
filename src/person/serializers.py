from rest_framework import serializers

from person.models import Student, Chef


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "net_id", "user", "favorite_eateries", "favorite_items"]


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ["id", "user", "eateries_managed"]
