from django.shortcuts import render
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from .models import Weather,Corn_grain_yield,DataAnalysis
import pandas as pd
import time
import csv 
from datetime import datetime,timedelta
from django.db.models import Avg
from django.db.models.functions.datetime import ExtractMonth, ExtractYear
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count

now = datetime.now()

from .serializers import WeatherDetailSerializer,Corn_grain_yieldDetailSerializer,DataAnalysisSerializer
# Create your views here.


def cutFile(f):
    output = " "
    for chunk in f.chunks():
        output += chunk.decode('ascii')
    return output.replace("\n", "").replace("\r", "")

class WeatherList(APIView):
    """
    List all campaign, or create a new campaign.    
    """
    
    def get(self, request, format=None):
        api_response = {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'failed', 'messages': [], 'data': []}
       
        paginator = PageNumberPagination()
        w_data = Weather.objects.all()
        context = paginator.paginate_queryset(w_data, request)
        serializer = WeatherDetailSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        f = r'./app/demo.txt'
        o = r'./app/demo.csv'
        parser_classes = (FileUploadParser,)
        # api_response = {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'failed', 'messages': [], 'data': []}
        try:
            start = datetime.now()

            my_file = request.FILES['txtfile']
            filename = '/tmp/myfile'
            with open(f, 'wb+') as temp_file:
                for chunk in my_file.chunks():
                    temp_file.write(chunk)


            # file_data = cutFile(request.FILES["txtfile"])
            # file_obj = open(f, "w")
            # file_obj.write(file_data)
            # print(file_data)
            with open(f, 'r') as in_file:
                lines = in_file.read().splitlines()
                stripped = [line.replace(","," ").split() for line in lines]
                grouped = zip(*[stripped]*1)
                with open(o, 'w') as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow(('date', 'max_temp', 'min_temp', 'precipitation '))
                    for group in grouped:
                        writer.writerows(group)
                # print(writer)

            time.sleep(2)
            products = []
            df =  pd.read_csv(o)
            
            # print(len(df))
            for i in range(len(df)):
                if Weather.objects.filter(dates =datetime.strptime(str(df.iloc[i][0]), '%Y%m%d')):
                    pass
                else:
                    products.append(
                        Weather(
                        dates = datetime.strptime(str(df.iloc[i][0]), '%Y%m%d'),
                        max_temp = int(df.iloc[i][1]),
                        min_temp = int(df.iloc[i][2]),
                        precipitation = int(df.iloc[i][3]),
                        )
                    )
            Weather.objects.bulk_create(products)
            end = datetime.now()
            execution_time =  end - start
            data = {"messages":"data added.","start_time":start,"end":end,"execution_time ":execution_time}
            return Response(data, status=status.HTTP_201_CREATED)
       
        except Exception as e:
            data=[]
            data["messages"]=str(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    


class Corn_grain_yieldList(APIView):
    """
    List all campaign, or create a new campaign.    
    """
    

    def get(self, request, format=None):
        api_response = {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'failed', 'messages': [], 'data': []}
       
        paginator = PageNumberPagination()
        w_data = Corn_grain_yield.objects.all()
        context = paginator.paginate_queryset(w_data, request)
        serializer = Corn_grain_yieldDetailSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        f = r'./app/demo1.txt'
        o = r'./app/demo1.csv'
        parser_classes = (FileUploadParser,)
        # api_response = {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'failed', 'messages': [], 'data': []}
        try:
            start = datetime.now()

            my_file = request.FILES['txtfile']
            with open(f, 'wb+') as temp_file:
                for chunk in my_file.chunks():
                    temp_file.write(chunk)

            with open(f, 'r') as in_file:
                lines = in_file.read().splitlines()
                stripped = [line.replace(","," ").split() for line in lines]
                grouped = zip(*[stripped]*1)
                with open(o, 'w') as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow(('year', 'harvested',))
                    for group in grouped:
                        writer.writerows(group)
                # print(writer)

            # time.sleep(2)
            products = []
            df =  pd.read_csv(o)
            
            # print(len(df))
            for i in range(len(df)):
                if Corn_grain_yield.objects.filter(year =str(df.iloc[i][0])):
                    pass
                else:
                    products.append(
                        Corn_grain_yield(
                        year = str(df.iloc[i][0]),
                        harvested = int(df.iloc[i][1]),
                        )
                    )
            Corn_grain_yield.objects.bulk_create(products)
            end = datetime.now()
            execution_time =  end - start
            data = {"messages":"data added.","start_time":start,"end":end,"execution_time ":execution_time}
            return Response(data, status=status.HTTP_201_CREATED)
       
        except Exception as e:
            data=[]
            data["messages"]=str(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    
class DataAnalysisList(APIView):
    def get(self, request, format=None):
        paginator = PageNumberPagination()
        w_data = DataAnalysis.objects.all()
        context = paginator.paginate_queryset(w_data, request)
        serializer = DataAnalysisSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)


    def post(self, request, format=None):
       
        try:
            start = datetime.now()
            w_data = list(Weather.objects.annotate(year=TruncYear('dates')).values("dates__year").annotate(max_temp_avg=Avg('max_temp'),min_temp_avg=Avg('min_temp'),total_precipitation=Count('precipitation')))
            
            products = []
            
            
            # print(len(df))
            for i in range(len(w_data)):
                if DataAnalysis.objects.filter(year =str(w_data[i]["dates__year"])):
                    pass
                else:
                    products.append(
                        DataAnalysis(
                        year = str(w_data[i]["dates__year"]),
                        max_temp_avg = w_data[i]["max_temp_avg"],
                        min_temp_avg = w_data[i]["min_temp_avg"],
                        total_precipitation = w_data[i]["total_precipitation"],
                        )
                    )
            DataAnalysis.objects.bulk_create(products)
            end = datetime.now()
            execution_time =  end - start
            data = {"messages":"data added.","start_time":start,"end":end,"execution_time ":execution_time}
            return Response(data, status=status.HTTP_201_CREATED)
       
        except Exception as e:
            data=[]
            data["messages"]=e
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
