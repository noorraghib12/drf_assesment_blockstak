from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Snippet
from .serializers import SnippetSerializer,SnippetModelSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view








# Create your views here.
@api_view(['GET','DELETE','POST'])
def snippet_list(request):
    if request.method == 'POST':
        json_data=JSONParser().parse(request)
        serialized = SnippetModelSerializer(data=json_)
        if serialized.is_valid():
            serialized.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(serialized.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        snippets=Snippet.objects.all()
        snippet_serials=SnippetModelSerializer(snippets,many=True)
        return Response(snippet_serials.data)
            


@api_view(['GET','PUT','DELETE'])
def snippet_details(request,pk,format=None):
    try:
        snippet=Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method=='GET':
        serialized=SnippetModelSerializer(snippet)
        return Response(serialized.data)
    elif request.method=='PUT':
        serialized=SnippetModelSerializer(snippet,data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data,status=status.HTTP_201_CREATED)
        return Response(serialized.data,status=status.HTTP_403_FORBIDDEN)
    elif request.method=="DELETE":
        serialized=SnippetModelSerializer(snippet)
        serialized.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


