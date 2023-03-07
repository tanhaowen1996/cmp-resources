from rest_framework import serializers
from .models import Nfs, VServer, Volume


class NfsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nfs
        fields = '__all__'


class VServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VServer
        fields = '__all__'


class VolumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volume
        fields = '__all__'
