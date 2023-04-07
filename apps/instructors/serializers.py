from rest_framework import serializers
from .models import Instructor, License
from apps.programs.models import Program


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'

    def to_representation(self, instance):
        representation = dict()
        representation["id"] = instance.id
        representation["instructor"] = instance.instructor.id
        representation["program"] = instance.program.id
        representation['licNum'] = instance.licNum
        representation["instructor_repr"] = instance.instructor.name
        representation["program_repr"] = instance.program.programName
        return representation

    
class InstructorSerializer(serializers.ModelSerializer):
    licenses = LicenseSerializer(many=True)

    class Meta:
        model = Instructor
        fields = '__all__'
        # read_only_fields = ['licenses']

    def create(self, validated_data):
        licenses_data = validated_data.pop('licenses')
        instructor = Instructor.objects.create(**validated_data)
        if len(licenses_data) > 0:
            for license_data in licenses_data:
                # if not License.objects.filter(id=license_data.id).exists():
                License.objects.create(instructor=instructor, **license_data)
        return instructor
    
    # no need to override update because in view
    # i set to partially update Instructor Serializer
    # def update(self, instance, validated_data):
    #     # instance is the current instance being edited
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.tel = validated_data.get('tel', instance.tel)
    #     instance.email = validated_data.get('email', instance.email)
    #     instance.address = validated_data.get('address', instance.address)
    #     instance.save()
    #     return instance
