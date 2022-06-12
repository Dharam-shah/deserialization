from django.shortcuts import render
from .models import Country, PetroleumProduct, Detail, Year
from rest_framework import viewsets
#from .serializers import CountrySerializer, PetroleumProductSerializer, DetailSerializer
import requests as r
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q, Sum
#-----------------------------------------
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


def get_data(input_field=None):
    response = r.get('https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json').json()
    data = []
    # country_class = []
    if input_field == 'country':
        for response_data in response:
            if response_data.get('country') not in data:
                data.append(response_data['country'])
                
    elif input_field == 'product':
        for response_data in response:
            if response_data.get('petroleum_product') not in data:
                data.append(response_data['petroleum_product'])
                
    elif input_field == 'year':
        for response_data in response: 
            if response_data.get('year') not in data:
                data.append(response_data['year'])
                
    else:
        dict_data = {}
        for response_data in response:
            dict_data['year'] = Year.objects.get(date = response_data['year']).id
            dict_data['petroleum_product'] = PetroleumProduct.objects.get(name= response_data['petroleum_product']).id
            dict_data['sale'] = response_data['sale']
            dict_data['country'] = Country.objects.get(name= response_data['country']).id
            data.append(dict_data)
            dict_data = {}
    return data


class CountryCreateView(APIView):
    models = Country
    
    def post(request, *args, **kwargs):
        data = get_data('country')
        for i in data:
            Country.objects.get_or_create(name = i)
        return Response(status=201)
    
class YearCreateView(APIView):
    models = Year
    
    def post(request, *args, **kwargs):
        data = get_data('year')
        for i in data:
            Year.objects.get_or_create(date = i)
        return Response(status=201)


class ProductCreateView(APIView):
    models = PetroleumProduct
    
    def post(request, *args, **kwargs):
        data = get_data('product')
        for i in data:
            PetroleumProduct.objects.get_or_create(name = i)
        return Response(status=201)


class DetailCreateView(APIView):
    models = Detail
    
    def post(request, *args, **kwargs):
        data = get_data()
        for i in data:
            Detail.objects.create(year = Year.objects.get(id = i.get('year')), country = Country.objects.get(id = i.get('country')), sale = i.get('sale'), petroleum_product= PetroleumProduct.objects.get(id =i.get('petroleum_product')))
        return Response(status=201)

class PoductSaleView(viewsets.ReadOnlyModelViewSet):
    
    def get_queryset(self):
        queryset = Detail.objects.values('petroleum_product').annotate(Total_sale =Sum('sale'))

        return queryset

class CountryWiseSaleView(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):

        high_country = Detail.objects.values('country__name').annotate(Sum('sale')).order_by('-sale')[:3]
        low_country = Detail.objects.values('country__name').annotate(Sum('sale')).order_by('sale')[:3]

        return high_country