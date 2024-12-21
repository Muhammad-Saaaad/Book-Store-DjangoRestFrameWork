from django.urls import path

from payment.views import *

urlpatterns = [
    path("checkout",checkout.as_view()),
    path("webhooks",my_webhook_view),

    path("success/", template_view.sucess_view, name="success"),
    path("cancel/", template_view.cancel_view, name="cancel"),
]