from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import AvansUser
from rest_framework import generics
from .serializers import UserSerializer,UserIdsSerializer
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q,Sum
from django.db import models
import pandas as pd
import os
from config.settings import MEDIA_ROOT
from django.views.decorators.csrf import csrf_exempt

class ListUsers(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        serializer = UserSerializer(AvansUser.objects.all(),many=True)
        return Response(serializer.data)

class UserIds(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        serializer = UserIdsSerializer(AvansUser.objects.all(),many=True)
        return Response(serializer.data)


class UserUpdate(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request,id, format=None):
        data = dict(request.data)
        if AvansUser.objects.filter(user_id =data['user_id'][0],oy=datetime.now().month).exists():
            user = AvansUser.objects.filter(user_id =data['user_id'][0],oy=datetime.now().month)[:1].get()
            user.avans = data['avans'][0]
            user.save()
        else:
            user = AvansUser.objects.filter(user_id =data['user_id'][0],oy=datetime.now().month)[:1].get()
            user.avans = data['avans'][0]
            user.save()
            
        serializer = UserIdsSerializer(AvansUser.objects.all(),many=True)
        return Response(serializer.data)

class CreateAvansUserView(generics.CreateAPIView):
    queryset = AvansUser.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class UserDelete(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        data = dict(request.data)
        if 'user_id' in data:
            if AvansUser.objects.filter(user_id=int(data['user_id'][0])).exists():
                user = AvansUser.objects.filter(user_id=int(data['user_id'][0]))
                user.delete()

        return Response({'msg':True})


class UserAvansSave(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        data = dict(request.data)
        if 'user_id' in data:
            if AvansUser.objects.filter(user_id=int(data['user_id'][0]),oy=datetime.now().month).exists():
                user = AvansUser.objects.filter(user_id=int(data['user_id'][0]),oy=datetime.now().month)[:1].get()
                user.avans = data['avans'][0]
                user.save()
            else:
                if AvansUser.objects.filter(Q(user_id=int(data['user_id'][0]))&~Q(name =None)).exists():
                    username =  AvansUser.objects.filter(Q(user_id=int(data['user_id'][0]))&~Q(name =None))[:1].get().name
                else:
                    username = data['name'][0]

                user = AvansUser(
                user_id = data['user_id'][0], 
                chat_id = data['chat_id'][0], 
                avans = data['avans'][0], 
                oy=datetime.now().month,
                name= username
                )
                user.save()

        return Response({'msg':True})


class UserAvansCheck(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self,request):
        data = dict(request.data)
        if 'user_id' in data:
            if AvansUser.objects.filter(Q(user_id=int(data['user_id'][0]))&Q(oy=datetime.now().month-1)&~Q(avans=None)).exists():
                user = AvansUser.objects.filter(Q(user_id=int(data['user_id'][0]))&Q(oy=datetime.now().month-1)&~Q(avans=None))[:1].get()
                new_up = AvansUser(
                user_id = user.user_id, 
                chat_id = user.chat_id, 
                avans = user.avans, 
                name= user.name
                )
                new_up.save() 
                return Response({'updated':True})
            else:
                return Response({'updated':False})
            


class GetUsersForMessage(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        user_ids_dict = list(AvansUser.objects.filter(Q(oy =datetime.now().month)&~Q(avans = None)).values('user_id').distinct())
        user_ids = [user['user_id'] for user in user_ids_dict]
        users_for_msg = AvansUser.objects.filter(~Q(user_id__in =user_ids)).values('user_id','chat_id').distinct()
        serializer = UserIdsSerializer(users_for_msg,many=True)
        return Response(serializer.data)

class GetPathExcel(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self,request):
        users = AvansUser.objects.filter(Q(oy=datetime.now().month)&~Q(avans=None)).values_list('name','avans')

        current_month = datetime.now().month
        avans_sum = AvansUser.objects.filter(oy=current_month).aggregate(total_avans=Sum('avans', output_field=models.DecimalField()))

        total_avans = avans_sum['total_avans'] if avans_sum['total_avans'] is not None else 0



        df1 = pd.DataFrame(
                list(users), columns=["Ф.И.О", "Аванс суммаси"]
            )
        df2 =pd.DataFrame({'Ф.И.О':['Итого :',],'Аванс суммаси':[total_avans,]})
        frames = [df1, df2]
        result = pd.concat(frames)
        result['№'] = range(1,len(result)+1)
        
        desired_order = ['№', 'Ф.И.О', 'Аванс суммаси']

        result = result[desired_order]

        now = datetime.now()
        minut =now.strftime("%Y-%B-%d %H_%M_%S")
        
        create_folder(f'{MEDIA_ROOT}',f'uploads')
        create_folder(f'{MEDIA_ROOT}\\uploads',minut)
        path =f'{MEDIA_ROOT}\\uploads\\{minut}\\SAP AVANS.xlsx'
        

        result['Аванс суммаси'] = result['Аванс суммаси'].astype(float).apply(format_with_thousands_separator)

        result.iloc[-1, result.columns.get_loc('№')] = ''
        result = result.reset_index(drop=True)
        result = result.style.apply(lambda x: ['font-weight: bold;border: 1px solid black' if x['Ф.И.О'] == 'Итого :' else 'border: 1px solid black' for _ in x], axis=1)
        
        result.to_excel(path,index=False)
        return Response({'path':path})

def add_border_style(val):
    return 'border: 1px solid black'

def format_with_thousands_separator(value):
    return '{:,.2f}'.format(value).replace(',', ' ').replace('.', ',')



def create_folder(parent_dir,directory):
    path =os.path.join(parent_dir,directory)
    if not os.path.isdir(path):
        os.mkdir(path)