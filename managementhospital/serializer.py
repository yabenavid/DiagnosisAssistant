from rest_framework import serializers
from .models import Hospital

class HospitalSerializer(serializers.ModelSerializer):
    hospital = serializers.SerializerMethodField()

    def get_hospital(self, obj):
        return obj.hospital.id if obj.hospital else None

    class Meta:
        model = Hospital
        fields = '__all__'