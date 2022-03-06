# from django.shortcuts import render
from django.contrib.auth.models import User
from room import models
import requests

from rest_framework import status
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken

# from django.contrib.auth.hashers import make_password
# from django.contrib.auth.base_user import BaseUserManager
import json
from .serializers import BorrowTimeSerializer, RoomSerializer
import datetime
# from django.http import HttpResponse, JsonResponse


class GoogleView(APIView):
    def post(self, request):
        data = request.data
        print(data)
        token = data['token']['access_token']
        # token = data['res']['wc']['access_token']
        payload = {'access_token': token}  # validate the token
        r = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)
        print(data)
        print(token)
        if 'error' in data:
            content = {
                'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist

        try:
            user = User.objects.get(
                username=data['email'], email=data['email'])

        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            user.email = data['email']
            user.save()
            user = User.objects.get(username=data['email'])
            profile = models.Profile.objects.create(
                email=data['email'], user=user)
            profile.save()
            print(user)
            # # provider random default password
            # # user.password = make_password(
            # # BaseUserManager().make_random_password())
        # generate token without username & password
        # token = RefreshToken.for_user(user)
        response = {}
        return Response(response)


class RoomModule(APIView):
    def post(self, request):
        r = request.data
        try:
            m = Module()
            room_function = r['function']
            resp = getattr(m, room_function)(r)
            return Response(resp)
        except Exception as e:
            print(e)
            return Response({'error': 'error'})
        return Response({'error': "error1"})

    def get(self, request):
        r = request.GET
        ip = request.META
        try:
            room_function = r['function']
            m = Module()
            resp = getattr(m, room_function)(r)
        except Exception as e:
            print(e)
            return Response({'error': 'error'})
        return Response(resp)


class Module(object):

    def get_room_data(self, r):
        login_status = self._check_token(r['access_token'])
        if(login_status.status_code != 200):
            return Response(status=login_status)

        room_name = r['room_name']
        day = datetime.datetime.now() - datetime.timedelta(days=1)
        room_id = models.Room.objects.get(name=room_name).id
        room_data = models.BorrowTime.objects.filter(
            start_time__gte=day, room=room_id)
        serializer = BorrowTimeSerializer(room_data, many=True)
        return serializer.data

    def get_user_borrow_data(self, r):
        login_status = self._check_token(r['access_token'])
        if(login_status.status_code != 200):
            return Response(status=login_status)

        user_name = r['userInfo']['user_name']
        user_id = models.Profile.objects.get(email=user_name).id
        user_borrow_data = models.BorrowTime.objects.filter(
            borrower=user_id).order_by('-start_time')
        serializer = BorrowTimeSerializer(user_borrow_data, many=True)

        return serializer.data

    def delete_user_borrow_data(self, r):
        login_status = self._check_token(r['access_token'])
        if(login_status.status_code != 200):
            return Response(status=login_status)
        borrower = r['data']['borrower']
        start_time = r['data']['start_time']
        end_time = r['data']['end_time']
        user_id = models.Profile.objects.get(email=borrower).id
        instance = models.BorrowTime.objects.get(
            borrower=user_id, start_time=start_time, end_time=end_time)
        instance.delete()
        return

    def get_room_page(self, r):
        room_page = models.Room.objects.all()
        serializer = RoomSerializer(room_page, many=True)
        return serializer.data

    def create_new_borrow(self, r):
        login_status = self._check_token(r['access_token'])
        if(login_status.status_code != 200):
            return Response(status=login_status)

        borrower = models.Profile.objects.get(email=r['data']['borrower'])
        room = models.Room.objects.get(name=r['data']['borrow_room'])
        start_time = "{} {}".format(
            r['data']['date'], r['data']['start_time']['time'])
        end_time = "{} {}".format(
            r['data']['date'], r['data']['end_time']['time'])
        borrow_reason = r['data']['borrow_reason']
        models.BorrowTime.objects.create(
            room=room,
            start_time=start_time,
            end_time=end_time,
            borrower=borrower,
            borrow_reason=borrow_reason)
        return

    def send_line_notify(self, r):
        headers = {
            "Authorization": "Bearer " + "///",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {"message": r['data']}

        r = requests.post("https://notify-api.line.me/api/notify",
                          headers=headers, params=params)
        return

    @staticmethod
    def _check_token(google_access_token):
        r = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo?access_token={}'.format(google_access_token))
        print(r)
        if r.status_code == 200:
            return Response(status=200)
        else:
            return Response(status=500)
