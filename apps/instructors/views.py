from django.http import Http404
# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# from apps.program import serializers
from .models import Instructor, License
from .serializers import InstructorSerializer, LicenseSerializer



class AllInstructorsList(APIView):
    def get(self, requset, format=None):
        allInstructors = Instructor.objects.all().order_by('name')
        serializer = InstructorSerializer(allInstructors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InstructorDetail(APIView):
    def get_object(self, pk):
        try:
            return Instructor.objects.get(pk=pk)
        except Instructor.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        instructor = self.get_object(pk)
        serializer = InstructorSerializer(instructor)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        instructor = self.get_object(pk)
        licenses = request.data.pop('licenses') # licenses property was popped out. 
        # print(request.data) # for debugging
        # partial update serializer 
        # licenses list is passed to InstructorSerializer
        serializer = InstructorSerializer(instructor, data=request.data, partial=True)
        # print("hello")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# return all licenses objects
class AllLicensesList(APIView):
    def get(self, request, format=None):
        allLicenses = License.objects.all().order_by('instructor__id')
        serializer = LicenseSerializer(allLicenses, many=True)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        serializer = LicenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# return all licenses that belong to a specific instructor
class InstructorLicenseList(APIView):
    def get(self, request, pk, format=None):
        allLicenses = License.objects.all()
        thisInstructorLicenses = allLicenses.filter(instructor__id=pk)
        serializer = LicenseSerializer(thisInstructorLicenses, many=True)
        return Response(serializer.data)