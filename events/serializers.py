from .models import event, advertise
from rest_framework import serializers

class eventBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = '__all__'
class eventHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ['id', 'title', 'sponsor_category', 'host', 'date', 'deadline', 'views', 'event_image']

class adSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertise
        fields = '__all__'

class adImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertise
        fields = ['id', 'ad_image']