
from django.urls import path

from reservation.views import TablesAPIView, ReservationAPIView

urlpatterns = [
    path('tables/', TablesAPIView.as_view(), name='tables-list'),  # GET, POST
    path('reservations/', ReservationAPIView.as_view(), name='reservations-list'),  # GET, POST
]