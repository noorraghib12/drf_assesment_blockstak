from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request):
    
        data=request.data
        data['user']=request.user.pk
        serializer=BlogSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status':400,
                'message':'Oops, something went wrong!',
                "data":serializer.errors
            })
        serializer.save()
        return Response({
        'message': "Blog created successfully.",
        'status':201,
        'data': serializer.data
        })
    def get(self,request):
        data=request.data
        blogs=Blog.objects.filter(user=request.user).all()
        serialized=BlogSerializer(blogs,many=True)
        return Response(serialized.data)
    
# class BlogCRUDView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     def put(self,request,pk,format=None):
#         data=request.data
#         data['user']=request.user.id
        
    
        