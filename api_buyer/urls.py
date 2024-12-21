from django.urls import path , include

from buyer.views import Shops, BuyShowBooks

urlpatterns= [
    path("show-all-shops", Shops.as_view()),
    path("buy-show-books", BuyShowBooks.as_view()),
]