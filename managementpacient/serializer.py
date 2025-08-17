# managementpacient/serializers.py
from rest_framework import serializers
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    hospital_id = serializers.IntegerField(source='hospital.id', read_only=True)
    download_url = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()

    class Meta:
        model = History
        fields = ['id', 'hospital_id', 'created_at', 'download_url', 'filename']

    def get_download_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(f'/api/v1/download-report/{obj.id}/') if request else None

    def get_filename(self, obj):
        return obj.s3_pdf_key.split('/')[-1]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('hospital_id', None)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return representation
