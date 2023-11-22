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
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage

from .models import event, advertise
from .serializers import eventBaseSerializer, adSerializer, adImageSerializer, eventHomeSerializer


class EventSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

@permission_classes([AllowAny]) # 아무나 가능
class ListViewSet(ReadOnlyModelViewSet):
    queryset = event.objects.all()
    serializer_class = eventHomeSerializer
    pagination_class = EventSetPagination

    @action(detail=False, methods=['get'])
    def views(self, request): # 조회순
        qs = self.queryset.order_by('-views')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def latest(self, request): # 최신순
        qs = self.queryset.order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def deadline(self, request): # 마감일순
        qs = self.queryset.order_by('deadline')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommends(self, request): # 추천순
        qs = self.queryset.order_by('-recommends')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class HomeAPIView(APIView): # 홈화면 데이터(광고, 이벤트) 전달
    permission_classes = [AllowAny] # 아무나 가능
    
    def get(self, request):
        events = event.objects.all().order_by('-views')
        if events.count() > 16:
            events = events[:16]
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
        serializer = eventBaseSerializer(data=data)
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


class EventDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None): # 행사 상세보기 및 조회수 증가
        instance = get_object_or_404(event, id=pk)
        serializer = eventBaseSerializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        if request.COOKIES.get('hit') is not None: # 쿠키에 hit 값이 이미 있을 경우
            cookies = request.COOKIES.get('hit')
            cookies_list = cookies.split('|')
            if str(pk) not in cookies_list:
                instance.views += 1
                instance.save()
                serializer = eventBaseSerializer(instance)
                response = Response(serializer.data, status=status.HTTP_200_OK)
                response.set_cookie('hit', cookies+f'|{pk}')
                    
        else: # 쿠키에 hit 값이 없을 경우(즉 현재 보는 게시글이 첫 게시글임)
            instance.views += 1
            instance.save()
            serializer = eventBaseSerializer(instance)
            response = Response(serializer.data, status=status.HTTP_200_OK)
            response.set_cookie('hit', pk)

        return response

class AdDetailAPIView(APIView):
    permission_classes=[AllowAny]

    def get(self, request, pk=None):
        instance = get_object_or_404(advertise, id=pk)
        serializer = adSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)