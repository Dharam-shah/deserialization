from django.urls import path,include
from .views import *
from django.db import router
from rest_framework.routers import DefaultRouter

#creating router obj
router=DefaultRouter()

#registering
# router.register('product',views.PetroleumProductView, basename='product')
# router.register('country',views.CountryView, basename='country')
# router.register('detail',views.DetailView, basename='detail'),
router.register('sale', PoductSaleView, basename='sale'),
# router.register('country-sale',views.SaleHignLowView, basename='country-sale')

urlpatterns = [
    # path('create/', views.create, name='create'),
    path('',include(router.urls)),
    path('country-create/', CountryCreateView.as_view()),
    path('product-create/', ProductCreateView.as_view()),
    path('year-create/', YearCreateView.as_view()),
    path('detail-create/', DetailCreateView.as_view()),
]




