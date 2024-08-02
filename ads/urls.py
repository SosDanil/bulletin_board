from django.urls import path

from ads.apps import AdsConfig
from ads.views import (AdListAPIView, AdCreateAPIView, AdDestroyAPIView, AdUpdateAPIVIew, AdRetrieveAPIView,
                       ReviewCreateAPIView, ReviewListAPIVIew, ReviewRetrieveAPIView, ReviewUpdateAPIView,
                       ReviewDestroyAPIView)

app_name = AdsConfig.name

urlpatterns = [
    path('', AdListAPIView.as_view(), name='ads_list'),
    path('create/', AdCreateAPIView.as_view(), name='ads_create'),
    path('retrieve/<int:pk>/', AdRetrieveAPIView.as_view(), name='ads_retrieve'),
    path('update/<int:pk>/', AdUpdateAPIVIew.as_view(), name='ads_update'),
    path('delete/<int:pk>/', AdDestroyAPIView.as_view(), name='ads_delete'),
    path('reviews/', ReviewListAPIVIew.as_view(), name='reviews_list'),
    path('reviews/create/', ReviewCreateAPIView.as_view(), name='reviews_create'),
    path('reviews/retrieve/<int:pk>/', ReviewRetrieveAPIView.as_view(), name='reviews_retrieve'),
    path('reviews/update/<int:pk>/', ReviewUpdateAPIView.as_view(), name='reviews_update'),
    path('reviews/delete/<int:pk>/', ReviewDestroyAPIView.as_view(), name='reviews_delete'),
]
