from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .serializers import ProgramSerializer
from .models import Program


class allProgramsList(APIView):
    def get(self, request):
        programs = Program.objects.all().order_by('programName')
        # many=True: queryset contains mutiple items (a list of items) 
        # data is list instead of an object
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        temp = request.data
        serializer = ProgramSerializer(data=temp)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProgramDetail(APIView):
    # by default get_object() method using self.kwargs["pk"] to search object.
    def get_object(self, pk):
        try:
            return Program.objects.get(pk=pk)
        except Program.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        program = self.get_object(pk)
        serializer = ProgramSerializer(program)
        return Response(serializer.data)