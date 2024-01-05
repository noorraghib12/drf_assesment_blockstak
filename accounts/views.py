from rest_framework.views import APIView
from rest_framework.response import Response
from .emails import *
from .serializer import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterAPI(APIView):
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
        response=serializer.get_jwt_token(data=request.data)

        return Response(response,status=200)
class Profileview(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]        
    def post(self,request):
        try:
            data=request.data
            data['user'] = request.user
            serializer=ProfileSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status':200,
                    'message':"Ooops, something went wrong!",
                    'data': serializer.errors
                })
        except Exception as e:
            print(e)
