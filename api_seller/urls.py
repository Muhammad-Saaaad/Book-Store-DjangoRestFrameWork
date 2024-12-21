from django.urls import path, include
from rest_framework.routers import DefaultRouter

from seller.views import *

# seller_router = DefaultRouter()
# seller_router.register('Seller', ShopView, basename='seller')

urlpatterns=[
    # path('crud-api', include(seller_router.urls))
    path('shop', ShopView.as_view()),
    path('book', BookView.as_view()),
]