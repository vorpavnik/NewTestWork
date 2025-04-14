import datetime

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from reservation.models import Tables, Reservation
from reservation.serializers import TablesSerializer, ReservationSerializer


class TablesAPIView(APIView):
    """APIView для столиков"""

    serializer = TablesSerializer

    def get(self, request):
        """Get с фильтрацией путем применения query-параметра
        status"""
        filter_busy = request.query_params.get('status', None)
        table_id = request.query_params.get('id')  # Получаем id из query parameters

        if table_id: # Если указан ID столика, возвращаем только его
            table = get_object_or_404(Tables, id=table_id)
            ser = self.serializer(table)
            return Response(ser.data)

        if filter_busy == 'busy': # Занятые столики
            tables = Tables.objects.filter(busyness=True).order_by('-id')
        elif filter_busy == 'free': # Свободные столики
            tables = Tables.objects.filter(busyness=False).order_by('-id')
        else:
            tables = Tables.objects.all().order_by('-id')  # Если нет параметра status - все столики
        ser = self.serializer(tables, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = self.serializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=201)
        return Response(ser.errors, status=400)

    def put(self, request):
        table_id = request.query_params.get('id')
        table = get_object_or_404(Tables, id=table_id)
        ser = self.serializer(table, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        return Response(ser.errors, status=400)

    def delete(self, request):
        table_id = request.query_params.get('id')
        table = get_object_or_404(Tables, id=table_id)
        table.delete()
        return Response(status=204)


class ReservationAPIView(APIView):

    serializer = ReservationSerializer

    def get(self, request):
        status_reservation = request.query_params.get('status', None)
        reservation_id = request.query_params.get('id')

        if reservation_id: # Если указан ID бронирования, возвращаем только его
            reservation = get_object_or_404(Reservation, id=reservation_id)
            ser = self.serializer(reservation)
            return Response(ser.data)

        if status_reservation == 'active':  # Активные бронирования
            reservations = Reservation.objects.filter(active=True).order_by('-id')
        elif status_reservation == 'inactive':  # Неактивные бронирования
            reservations = Reservation.objects.filter(active=False).order_by('-id')
        else:
            reservations = Reservation.objects.all().order_by('-id')  # Все бронирования без квери парамента
        ser = self.serializer(reservations, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = self.serializer(data=request.data)
        if ser.is_valid():
            table_id = ser.validated_data['table_id']
            if table_id.busyness:  # Если busyness=True, столик занят
                return Response(
                    {"error": "Этот столик уже занят. Пожалуйста, выберите другой."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Получаем reservation_time из validated_data
            reservation_time = ser.validated_data['reservation_time']
            # Сделаем datetime aware, если он naive
            if timezone.is_naive(reservation_time):
                reservation_time = timezone.make_aware(reservation_time,
                                                         timezone=timezone.get_current_timezone())

            ser.validated_data['reservation_time'] = reservation_time
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        res_id = request.GET.get('id')
        res = get_object_or_404(Reservation, id=res_id)
        ser = self.serializer(res, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(data=ser.data, status=200)
        return Response(ser.errors, status=400)

    def delete(self, request):
        res_id = request.query_params.get('id')
        res = get_object_or_404(Reservation, id=res_id)
        res.delete()
        return Response(status=204)