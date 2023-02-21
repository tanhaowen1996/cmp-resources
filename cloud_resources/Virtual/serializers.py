from rest_framework import serializers
from .models import Nfs, VServer


class NfsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nfs
        fields = '__all__'


class VServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = VServer
        fields = '__all__'
