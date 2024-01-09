from rest_framework.views import APIView
from rest_framework.response import Response
from .emails import *
from .serializer import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterAPI(APIView):
    """
    REGISTRATION API
    """

    def post(self,request):
        data=request.data
        verification_serialized=RegisterSerializer(data=data)
        if verification_serialized.is_valid():
            verification_serialized.save()
            send_otp_via_email(email=verification_serialized.data['email'])
            return Response({
                'status': 200,
                'message': "Registration Partially Complete, Please check registered email for account verification",
                'data' : {}
            })
    
        return Response({
            'status': 400,
            'message': "Something went wrong.",
            'data' : verification_serialized.errors
        })


class VerifyRegistrationAPI(APIView):
    """
    VERIFY REGISTRATION API
    """
    def post(self,request):
        verify_data=request.data
        verification_serialized=VerifyAccountSerializer(data=verify_data)
        if verification_serialized.is_valid():
            verify_email=verification_serialized.data['email']
            verify_email_verification_token=verification_serialized.data['email_verification_token']
            try:
                user = User.objects.get(email=verify_email)
            except user.DoesNotExist:
                return Response({
                    'status':404,
                    'message': 'Sorry, something went wrong',
                    'data':'Invalid Email'
                })

            if user.email_verification_token == verify_email_verification_token:
                user.is_verified=True
                user.save()
                return Response({
                    'status':200,
                    'message':'User Successfully verified!'
                })
            else:
                return Response({
                    'status':400,
                    'message':'Sorry, something went wrong!',
                    'data':"Verficiation token provided isn't correct."
                })
            

        else:
            return Response({
                'status':status.HTTP_400_BAD_REQUEST,
                'message': "Oops something went wrong!",
                'data':verification_serialized.errors
            })

class LoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'status':400,
                'data':serializer.errors,
                'message':"Something went wrong!"
            })
        # if not User.object.get(data['username']).is_verified:
        #     return Response({
        #         'status':400,
        #         'data':serializer.errors,
        #         'message':"Sorry, user not verified!"
        #     })

        response=serializer.get_jwt_token(data=request.data)

        return Response(response,status=200)


class ProfileWriteview(APIView):
    """ CRUD OPERATIONS FOR USER PROFILE"""


    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]        
    def post(self,request):
        try:
            data=request.data.copy()
            data['user'] = request.user.id
            serializer=ProfileSerializer(data=data)
            if not serializer.is_valid(): 
                return Response({
                    'status':400,
                    'message':"Ooops, something went wrong!",
                    'data': serializer.errors
                })
            else:
                return Response({
                    'status':200,
                    'message':"Profile data created!",
                    'data': serializer.data
                })
                serializer.save()
        except Exception as e:
            print(e)
            return Response({
                'status': 400,
                'message': "Ooops something went wrong",
                'data':{'error':e}
            })

    def patch(self,request):
        data=request.data.copy()
        data['user']=request.user.id
        serializer=ProfileSerializer(data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status":201,
                "message":"Profile information has been updated!", 
                "data":serializer.data
            })
        else:
            return Response({
                "status":400,
                'message':"Sorry, there were some issues fetching the data!",
                'data':serializer.data
            })



class ProfileGetview(APIView):
    """
    PUBLIC PROFILE VIEW 
    """
    def get(self,request,username):
        if username=='me':
            username=request.user.username
        
        user=User.objects.filter(username=username)
        if not user.exists():
            return Response({
                'status':404,
                'message':f"No user named {username} exists within our database",
                'data':{}
            })
        
        
        profile=Profile.objects.filter(user=user.first())
        if not profile.exists():
            return Response({
                "status":404,
                "message": "Sorry, this user has not updated their profile",
                "data": "Profile doesnt exist"
            })
        # profile_data=profile[0]
        # profile_data['user']=request.user.id
        
        serializer=ProfileSerializer(profile.first())
        # if serializer.is_valid():
        return Response({
            'status':200,
            'message':"Profile fetched!",
            'data':serializer.data
        })

