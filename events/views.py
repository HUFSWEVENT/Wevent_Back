import json

from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.decorators import action
from rest_framework.decorators import permission_classes

from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage

from .models import event, advertise
from .serializers import eventRegisterSerializer, adSerializer, adImageSerializer, eventHomeSerializer

@permission_classes([AllowAny]) # 아무나 가능
class ListViewSet(ReadOnlyModelViewSet):
    queryset = event.objects.all()
    serializer_class = eventHomeSerializer

    @action(detail=False, methods=['get'])
    def views(self, request): # 조회순
        qs = self.queryset.order_by('-views')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request): # 최신순
        qs = self.queryset.order_by('-created_at')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def deadline(self, request): # 마감일순
        qs = self.queryset.order_by('deadline')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommends(self, request): # 추천순
        qs = self.queryset.order_by('-recommends')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class HomeAPIView(APIView): # 홈화면 데이터(광고, 이벤트) 전달
    permission_classes = [AllowAny] # 아무나 가능
    
    def get(self, request):
        events = event.objects.all().order_by('-views')
        if events.count() > 48:
            events = events[:48]
        ad = advertise.objects.all()

        e_serializer = eventHomeSerializer(events, many=True)
        a_serializer = adImageSerializer(ad, many=True)

        res = Response(
            {
                "ads" : a_serializer.data,
                "events" : e_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
        return res

class RegisterEventAPIView(APIView):
    permission_classes = [AllowAny] # 로그인 상태일때만 허용해야됨

    #행사 등록
    # @csrf_exempt # csrf 적용 안시키는건데 로그인 기능 생기면 삭제
    def post(self, request):
        data = json.loads(request.data['data'])
        serializer = eventRegisterSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            # serializer.save(user = request.user.email) # jwt 인증하고 받은 user객체의 이메일 알아내고 같이 저장해야할듯
            if request.FILES['event_image']:
                uploaded_event = request.FILES["event_image"]
                # fs = FileSystemStorage(
                #     location="media/event", base_url="/event"
                # )
                uploaded_event.name = str(event.id) + '.png' # 나중에 사진 수정할 때 찾아서 지우기위해 이름 설정
                # filename = fs.save(uploaded_event.name, uploaded_event)
                # uploaded_event_url = fs.url(filename)
                # serializer.save(event_image = uploaded_event_url)
                serializer.save(event_image = uploaded_event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

