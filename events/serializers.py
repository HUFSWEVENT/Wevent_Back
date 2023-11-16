from .models import event, advertise
from rest_framework import serializers

class eventSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = ['title', 'sponsor_category', 'host', 'date', 'deadline', 'views', 'event_image']

class adSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertise
        fields = '__all__'