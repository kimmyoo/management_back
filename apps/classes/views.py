from django.shortcuts import render
from rest_framework.views import APIView
from .models import Class, Student
from apps.instructors.models import License
from apps.programs.models import Program
from .serializers import ClassSerializer, StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# # # # # # # # # # # # # # # # # # 
#          all classes            #
#                                 #
# # # # # # # # # # # # # # # # # # 
class AllClassesList(APIView):
    def get(self, request, format=None):
        classes = Class.objects.all().order_by('license')
        serializer = ClassSerializer(classes, many=True)
        # print(serializer.data)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # # # # # # # # # # # # # # # # # 
#          Class Detail           #
#                                 #
# # # # # # # # # # # # # # # # # # 
class ClassDetail(APIView):
    # by default get_object() method using self.kwargs["pk"] to search object.
    def get_object(self, pk):
        try:
            return Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print(pk)
        clss = self.get_object(pk)
        serializer = ClassSerializer(clss)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        # print(request.data) # for debugging
        clss = self.get_object(pk)
        id= request.data.pop('license') # licenses property was popped out. 
        licInstance = License.objects.get(id=id)
        # print(licenseData['licNum'])
        # print(clss.license.licNum)
        if id != clss.license:
            clss.license = licInstance
            clss.save()
        serializer = ClassSerializer(clss, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# # # # # # # # # # # # # # # # # # 
#            all students         #
#                                 #
# # # # # # # # # # # # # # # # # # 
class AllStudentsList(APIView):
    def get(self, request, format=None):
        students = Student.objects.all().order_by('id')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # # # # # # # # # # # # # # # # # 
#          student detail         #
#                                 #
# # # # # # # # # # # # # # # # # # 
class StudentDetail(APIView):
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)


# # # # # # # # # # # # # # # # # # 
#  Students in a class list       #
#                                 #
# # # # # # # # # # # # # # # # # # 
class StudentsInClassList(APIView):
    # when trying to get object from database, 
    # use try except block
    def get_object(self, pk):
        try:
            return Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        clss = self.get_object(pk)
        # correct way of many to many field filtering
        students = Student.objects.filter(classes=clss).order_by('lName', 'fName')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    

# # # # # # # # # # # # # # # # # # 
#  classes taken by the student   #
#                                 #
# # # # # # # # # # # # # # # # # # 
class ClassesTakenByStudent(APIView):
    def get_studentObject(self, pk):
        try: 
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_studentObject(pk)
        classes = student.classes.all()
        # don't forget the many=True is it's a list
        # leaving many=True caused a bug!
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

# # # # # # # # # # # # # # # # # # 
#  classes of the same program    #
#                                 #
# # # # # # # # # # # # # # # # # # 
class ClassesInProgramList(APIView):
    def get(self, request, pk, format=None):
        # program = self.get_programObject(pk)
        classes = Class.objects.filter(program=pk).order_by('updatedAt', 'code')
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
