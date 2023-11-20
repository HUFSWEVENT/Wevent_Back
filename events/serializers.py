from .models import event, advertise
from rest_framework import serializers

class eventRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = '__all__'
class eventHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ['title', 'sponsor_category', 'host', 'date', 'deadline', 'views', 'event_image']

class adSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertise
        fields = '__all__'

class adImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertise
        fields = ['ad_image']