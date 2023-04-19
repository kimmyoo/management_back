from django.shortcuts import render
from rest_framework.views import APIView
from .models import Class, Student
from apps.instructors.models import License
from apps.programs.models import Program
from .serializers import ClassSerializer, StudentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from datetime import datetime, timedelta, time 
from users.utils.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes
# from rest_framework.permissions import IsAdminUser


# # # # # # # # # # # # # # # # # # 
#          all classes            #
#                                 #
# # # # # # # # # # # # # # # # # # 
@authentication_classes([JWTAuthentication])
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
@authentication_classes([JWTAuthentication])
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
        
        if id != clss.license.id:
            clss.license = licInstance
            clss.save()
        serializer = ClassSerializer(clss, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# # # # # # # # # # # # # # # # # # 
#            all students         #
#     (recently updated students) #
# # # # # # # # # # # # # # # # # # 
@authentication_classes([JWTAuthentication])
class AllStudentsList(APIView):
    def get(self, request, format=None):
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())

        # students with no class association and students updated today.  .order_by('id')  .order_by('updatedAt')
        studentsNoClass = Student.objects.filter(classes=None)
        studentsUpdatedToday = Student.objects.filter(updatedAt__lte=today_end, updatedAt__gte=today_start)
        # print(studentsUpdatedToday)
        # students = studentsUpdatedToday|studentsNoClass
        students = studentsUpdatedToday.union(studentsNoClass)
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
#      get, put                   #
# # # # # # # # # # # # # # # # # # 
@authentication_classes([JWTAuthentication])
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

    def put(self, request, pk, format=None):
        student = self.get_object(pk)
        # get the ids in a list
        originalClassList = list (student.classes.all().values_list('id', flat=True))
        requestClassList = request.data.pop('classes')
        
        # frontend added new class, requestedClassList is a string of class code
        if not isinstance(requestClassList, list):
            try:
                clss = Class.objects.get(code=requestClassList)
                student.classes.add(clss)
            except Class.DoesNotExist:
                raise Http404
        # frontend deleted classes. 
        elif len(requestClassList) < student.classes.count():
            deletedIDs = list(set(originalClassList) - set(requestClassList))
            try:
                for id in deletedIDs:
                    clss = Class.objects.get(id=id)
                    student.classes.remove(clss)
            except Class.DoesNotExist:
                raise Http404
        
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        if request.user.is_superuser:
            student = self.get_object(pk)
            student.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            content = {"Permission": "reguler user cannot delete"}
            return Response(content, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# # # # # # # # # # # # # # # # # # 
#  Students in a class list       #
#                                 #
# # # # # # # # # # # # # # # # # # 
@authentication_classes([JWTAuthentication])
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
@authentication_classes([JWTAuthentication])
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
#  Ten classes of each program    #
# # # # # # # # # # # # # # # # # # 
@authentication_classes([JWTAuthentication])
class ClassesInProgramList(APIView):
    def get(self, request, pk, format=None):
        # program = self.get_programObject(pk)
        classes = Class.objects.filter(program=pk).order_by('-begin')
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

@authentication_classes([JWTAuthentication])
class TenClassesInProgramList(APIView):
    def get(self, request, format=None):
        # this is how to initialize empty queryset of a model
        classQuerySet = Class.objects.none()
        programs = Program.objects.all()
        if len(programs) > 0:
            for program in programs:
                tenClassesQuerySet = Class.objects.filter(program=program).order_by('-createdAt')[:10]
                # union method returns a new set, 
                # but it doesn't change the current set(s). 
                # You need to (re)assign the result
                classQuerySet = classQuerySet|tenClassesQuerySet
        serializer = ClassSerializer(classQuerySet, many=True)
        return Response(serializer.data)

