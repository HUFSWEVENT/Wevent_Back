# Generated by Django 4.2.6 on 2023-11-14 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='행사명')),
                ('host', models.CharField(max_length=20, verbose_name='주최사명')),
                ('host_email', models.EmailField(max_length=50, verbose_name='주최사 이메일')),
                ('field', models.CharField(max_length=10, verbose_name='행사분야')),
                ('category', models.CharField(max_length=10, verbose_name='행사유형')),
                ('size', models.CharField(max_length=10, verbose_name='행사규모')),
                ('introduce', models.TextField(verbose_name='행사소개')),
                ('date', models.DateTimeField(verbose_name='행사날짜')),
                ('on_off', models.CharField(max_length=10, verbose_name='온오프라인')),
                ('deadline', models.DateTimeField(verbose_name='협찬마감일')),
                ('detail_location', models.CharField(max_length=30, verbose_name='상세주소')),
                ('sponsor_category', models.CharField(max_length=20, verbose_name='협찬 종류')),
                ('sponsor_advantage', models.TextField(verbose_name='협찬 혜택')),
                ('event_image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='행사 대표 이미지')),
                ('participant', models.TextField(blank=True, verbose_name='참가자 기술')),
                ('participant_recruit', models.TextField(blank=True, verbose_name='참가자 모집 방법')),
                ('last_event', models.TextField(blank=True, verbose_name='행사 기록')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
            ],
        ),
    ]
