import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage

from random import *

def create_code(): # 보안코드 생성
    code = ''
    for i in range(6):
        if i % 2 == 0:
            c = randint(97,122)
        else:
            c = randint(48,57)
        code += chr(c)
    return code

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs"
                },
                status=status.HTTP_200_OK,
            )
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AuthAPIView(APIView):
    permission_classes = [AllowAny]
    # 유저 정보 확인
    def get(self, request):
        try:
            user = request.user
            serializer = UserSerializer(instance=user)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        except(AttributeError):
            return Response({"message": "No token"}, status=status.HTTP_400_BAD_REQUEST)
        
    # 로그인
    def post(self, request):
        # 유저 인증
        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            # res.set_cookie("access", access_token, httponly=True, samesite=None, secure=True)
            res.set_cookie("refresh", refresh_token, httponly=True, samesite=None, secure=True)
            return res
        else:
            return Response({"message": "wrong email or password or is not active zz"}, status=status.HTTP_400_BAD_REQUEST)

    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        data = {'refresh': request.COOKIES.get('refresh', None)}
        if data['refresh'] == None:
            return Response({"message": "Not login state"}, status=status.HTTP_400_BAD_REQUEST)
        response = Response({
            "message": "Logout success"
            }, status=status.HTTP_202_ACCEPTED)
        
        refresh_token = RefreshToken(data['refresh'])
        refresh_token.blacklist() # refresh_token은 blacklist로 못 쓰게하기
        # response.delete_cookie("access") # access 토큰은 쿠키에 저장을 안했었음
        response.delete_cookie("refresh")
        return response
        

class EmailAuthAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request): # 이메일 인증을 위한 보안코드 발송
        serializer = CodeForAuthSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            get_object_or_404(User, email=email)
            pre_instance = CodeForAuth.objects.filter(email=email)
            if pre_instance: # 보안코드를 계속 발송했을 때 같은 email 객체가 여러개 생길 것을 방지
                pre_instance.delete()
            code = create_code()
            serializer.save(code=code) # 보안코드까지 생성 후 한번에 저장
            subject = "위벤트 이메일 인증 보안코드입니다."
            message = "보안코드는 "+ code + " 입니다."
            to = [email]
            # if not to[0].endswith('@naver.com'):
            #     return Response({"message": "not naver mail"}, status=status.HTTP_400_BAD_REQUEST)
            EmailMessage(subject=subject, body=message, to=to).send()
            return Response({"message": "send code success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request): # 보안코드 비교 및 임시토큰 발행
        email = request.data.get("email")
        code = request.data.get("code")
        if email == None or code == None:
            return Response({"message": "no email or code"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(CodeForAuth, email=email)
        if code == instance.code:
            user = get_object_or_404(User, email=email)
            if user.is_active == False: # 인증했으면 활성화 해주기
                user.is_active = True
                user.save()
            token = TokenObtainPairSerializer.get_token(user) # 임시적으로 access 토큰만 발행
            refresh_token = str(token)
            access_token = str(token.access_token)
            refresh_token = RefreshToken(refresh_token)
            refresh_token.blacklist() # refresh_token은 blacklist로 못 쓰게하기
            res = Response(
                {
                    "message": "code is correct",
                    "access": access_token,
                },
                status=status.HTTP_200_OK,
            )
            instance.delete() # 보안코드를 올바르게 작성했을 경우 email 객체 삭제
            return res
        return Response({"message": "wrong code"}, status=status.HTTP_400_BAD_REQUEST)
    

class TokenRefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request): # 토큰 재발급(쿠키에서 알아서 처리하도록)
        data = {'refresh': request.COOKIES.get('refresh', None)}
        if data['refresh'] == None:
            return Response({"message": "No refresh_token in cookie"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TokenRefreshSerializer(data=data)
        if serializer.is_valid():
            access = serializer.validated_data.get('access', None)
            return Response({"access": access})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PwResetAPIView(APIView):
    def post(self, request): # pw 변경
        user = request.user
        password = request.data.get("password", None)
        if password == None:
            return Response({"message": "No password key"}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message": "password changed."}, status=status.HTTP_202_ACCEPTED)