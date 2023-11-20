from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


# class Location:
#     def __init__(self, latitude, longitude):
#         self.latitude = latitude
#         self.longitude = longitude

# class LocationField(MultiValueField):
#     def __init__(self, *args, **kwargs):
#         fields = (
#             FloatField(max_value=90, min_value=-90),
#             FloatField(max_value=90, min_value=-90)
#         )
#         super().__init__(*args, **kwargs)


#     def compress(self, data_list):
#         latitude, longitude = data_list
#         return Location(latitude, longitude)


class event(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField('행사명', max_length=20)
    host = models.CharField('주최사명', max_length=20)
    host_email = models.EmailField('주최사 이메일', max_length=50)
    field = models.CharField('행사분야', max_length=10)
    category = models.CharField('행사유형', max_length=10)
    size = models.CharField('행사규모', max_length=10)
    introduce = models.TextField('행사소개')
    date = models.DateTimeField('행사날짜', auto_now = False , auto_now_add = False)
    on_off = models.CharField('온오프라인', max_length=10)
    deadline = models.DateTimeField('협찬마감일', auto_now = False , auto_now_add = False)
    # location = models.CharField('행사장소', max_length=30) # 위도 경도로 받으면 좋긴 함
    detail_location = models.CharField('상세주소', max_length=30)
    sponsor_category = models.CharField('협찬 종류', max_length=20)
    sponsor_advantage = models.TextField('협찬 혜택')
    event_image = models.ImageField('행사 대표 이미지', upload_to='event/', null =True, blank=True)
    participant = models.TextField('참가자 기술', blank=True)
    participant_recruit = models.TextField('참가자 모집 방법', blank=True)
    last_event = models.TextField('행사 기록', blank=True)
    created_at = models.DateTimeField('생성일', auto_now_add = True)
    views = models.IntegerField('조회수', default=0)
    recommends = models.IntegerField('추천정도',default=0)

class advertise(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField('광고제목', max_length=20)
    host = models.CharField('광고협찬사', max_length=20)
    host_email = models.EmailField('광고협찬사 이메일', max_length=50)
    content = models.TextField('상세내용')
    ad_image = models.ImageField('광고 이미지', upload_to='ad/', null =True, blank=True)