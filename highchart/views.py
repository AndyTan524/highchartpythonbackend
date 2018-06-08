# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required

#Rest_Framework
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
# Create your views here.
import json
import math


@api_view(['POST'])
def kchartcomp(request):
    print(request.data)
    company = request.data['company']
    period = request.data['period']
    start_date = request.data['start_date']
    end_date = request.data['end_date']
    count = request.data['count']

    # For Real
    query = './media/image/' + company + '/' + period + '/' + count + '/' + start_date + '.png'
    
    # For Test

    query = 'http://192.168.1.134:8000/api/media/image/'+ company + '/'+ period + '/' + count + '/1.png'
    # print(query)
    # query = './media/image1/2.png'
    # query = 'image1/quotes_2017-12-29-14-20_2017-12-29-14-25.png'

    # Retrieval(query)
    # e = time.time()
    # print(e-s)
    return HttpResponse(query)

@api_view(['POST'])
def kchartdata(request):
    '''
        1: open
        2: low
        3: high
        4: close
    '''

    company = request.data['company']
    period = request.data['period']
    data = request.data['data']
    # print(company)
    # print(period)
    # print(data)

    filepath = './media/'+company+'/1.json'
    jsonfile = open(filepath)
    jsonfile = jsonfile.read()
    jsondata = json.loads(jsonfile)
    # print(jsondata)
    minvalue = 999999.0
    saved_id = 0
    for i in range(0, len(jsondata[period]) - len(data) + 1):
        dist = calculate_distance(data, jsondata[period], i)
        print(dist)
        if(minvalue > dist):
            minvalue = dist
            saved_id = i
    print(minvalue)
    print(saved_id)
    result = []
    for i in range(saved_id, saved_id + len(data)):
        item = {}
        item['date'] = jsondata[period][i][0]
        item['open'] = jsondata[period][i][1]
        item['high'] = jsondata[period][i][3]
        item['low']  = jsondata[period][i][2]
        item['close']= jsondata[period][i][4]
        result.append(item)
    return Response({'data' : result})

def calculate_distance(data, json_data, start_id):
    # print(data)
    # print("JSONDATA")
    # print(json_data)
    sum_distance = 0.0
    # print('len', len(data))
    for i in range(start_id, start_id + len(data)):
        distance = 0.0
        for j in range(0, 4):
            dis = data[i - start_id][j] - json_data[i][j+1]
            distance = dis * dis
        # print("distance", distance)
        sum_distance += distance
    # print("sum_distance", sum_distance)
    return sum_distance