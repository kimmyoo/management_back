from rest_framework import serializers
from .models import Class, Student
from apps.instructors.serializers import LicenseSerializer
from apps.programs.serializers import ProgramSerializer



class StudentSerializer(serializers.ModelSerializer):
    # classes = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Student
        fields = '__all__'


    # 
    def create(self, validated_data):
        classCodes = validated_data.pop('classes')
        student = Student.objects.create(**validated_data)
        if len(classCodes) > 0:
            for code in classCodes:
                # objects.get() is used when you are pretty sure 
                # that there is only one result.
                match = Class.objects.get(code=code)
                student.classes.add(match)
        student.save()
        return student


class ClassSerializer(serializers.ModelSerializer):
    # students = StudentSerializer()
    # license = LicenseSerializer()
    # program = ProgramSerializer()
    class Meta:
        model = Class
        fields = "__all__"