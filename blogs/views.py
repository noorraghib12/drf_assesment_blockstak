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
from django.core.paginator import Paginator
from accounts.models import User
class PublicBlogView(APIView):

    def get(self,request,username,format=None):
        """
        Fetch all user blogs for public viewing
        """
        try:
            data=request.data

            #If search keyword provided : Only fetch blogs with search keyword
            if username=='me':
                blogs=Blog.objects.filter(user=request.user)
            
            else:
                user=User.objects.filter(username=username)
                if not user.exists():
                    return Response({
                        'status':404,
                        'message': "Sorry, no user of this username exists"
                    })
                    
                blogs=Blog.objects.filter(user=user.first())
            if data.get('search'):
                search = data.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search)).all()
            

            page_number=request.GET.get('page',1)
            paginator = Paginator(blogs,2)
            serializer=BlogSerializer(paginator.page(page_number),many=True)
            return Response({
                'data':serializer.data,
                'message':f'{len(serializer.data)} Blogs fetched successfully.',
                'status':200
                })
        except Exception as e:
            print(e)
            return Response({
                'data':e,
                'message':"Something went wrong or invalid page.",
                'status' : 400
            })    






#BLOG CRUD API
class BlogView(APIView):

    """
    JWT Authenticated Simple Blog CRUD
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        """
        Post user written blogs, authenticated by JWT
        """

        data=request.data.copy()
        data['user']=request.user.id
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
        """
        Fetch user specific blogs, along with search functionality 
        if search keyword provided in request
        """

        data=request.data
        #If UID provided in request : Only fetch specific blog
        #If search keyword provided : Only fetch blogs with search keyword
        blogs=Blog.objects.filter(user=request.user)
        
        if data.get('search'):
            search = data.get('search')
            blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search)).all()
        
        if data.get('uid'):
            blogs=blogs.filter(uid=data.get('uid'))
        
        serializer=BlogSerializer(blogs,many=True)
        return Response({
            'data':serializer.data,
            'message':f'{len(serializer.data)} Blogs fetched successfully.',
            'status':200
            })
    

    def patch(self,request):
        """
        Edit user written blogs only if requested for edit by
        respective author of the blog.
        """

        data=request.data.copy()
        blog = Blog.objects.filter(uid=data['uid'])
        if not blog.exists():
            return Response({
                'data': {},
                'message': "The particular blog you were looking does not exist presently/anymore.",
                'status':status.HTTP_400_BAD_REQUEST
            })
        #Only allow patching when authenticated user is the author of the blog
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

    def delete(self,request):

        """
        Delete user blog when requested by blog author only
        """
        data=request.data.copy()
        blog=Blog.objects.filter(uid=data['uid'])
        if not blog.exists():
            return Response({
                'data': {},
                'message': "Invalid blog uid",
                'status':status.HTTP_400_BAD_REQUEST
            })
        
        # Requests for deleting blogs  that are not from blog author will be denied
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

            


     
    
        