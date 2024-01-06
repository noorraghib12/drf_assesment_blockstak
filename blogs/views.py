from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *
from rest_framework import status
from.models import Blog
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view
from django.db.models import Q
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
        blogs=Blog.objects.all()
        if request.GET.get('search'):
            search = request.GET.get('search')
            blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search)).all()

        serialized=BlogSerializer(blogs,many=True)
        return Response({'data':serialized.data,'message':'Blogs fetched successfully.','status':200})
    
    def patch(self,request):
        try: 
            data=request.data
            blog = Blog.objects.filter(uid=data['uid'])
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': "The particular blog you were looking does not exist presently/anymore.",
                    'status':status.HTTP_400_BAD_REQUEST
                })
            if request.user != blog[0].user:
                return Response({
                    'data': {},
                    'message': "You are not authorized to do this.",
                    'status':status.HTTP_400_BAD_REQUEST
                })
            serializer=BlogSerializer(blog[0],data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': "Blog successfully updated",
                    'status':status.HTTP_206_PARTIAL_CONTENT
                })
                
            else:
                return Response({
                    'data': serializer.errors,
                    'message': "Something went wrong, sorry.",
                    'status':status.HTTP_400_BAD_REQUEST
                })
        except Exception as e:
            print(e)
            return Response({
                    'data': {},
                    'message': "Something went wrong, sorry.",
                    'status':status.HTTP_400_BAD_REQUEST
                })
    def delete(self,request):
        data=request.data
        blog=Blog.objects.filter(uid=data['uid'])
        if not blog.exists():
            return Response({
                'data': {},
                'message': "Invalid blog uid",
                'status':status.HTTP_400_BAD_REQUEST
            })
        if request.user!=blog[0].user:
            return Response({
                'data': {},
                'message': "You are not authorized to do this",
                'status':status.HTTP_400_BAD_REQUEST
            })
        blog[0].delete()
        return Response({
            'data':{},
            'message': "blog has been successfully deleted",
            'status': status.HTTP_204_NO_CONTENT
        })

            


# @api_view(['GET','DELETE','PATCH'])
# def blog_details(request):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     try:
#         Blog.objects.get(user=request.user)
#     if request.method==[]
    
# class BlogCRUDView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     def put(self,request,pk,format=None):
#         data=request.data
#         data['user']=request.user.id
        
    
        