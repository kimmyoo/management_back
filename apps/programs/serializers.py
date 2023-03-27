from rest_framework import serializers
from .models import Program
from apps.instructors.models import License
from apps.instructors.serializers import LicenseSerializer

class ProgramSerializer(serializers.ModelSerializer):
    licenses = LicenseSerializer(many=True)
    
    class Meta:
        model = Program
        fields = '__all__'

    # since Program is the FK of License
    # it involves nested serializer
    # need to redefine FK's create() method 

    def create(self, validated_data):
        licenses_data = validated_data.pop('licenses')
        program = Program.objects.create(**validated_data)
        if len(licenses_data) > 0:
            for license_data in licenses_data:
                License.objects.create(program=program, **license_data)
        return program