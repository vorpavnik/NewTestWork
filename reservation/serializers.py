import datetime

from django.utils import timezone
from rest_framework import serializers
from reservation.models import Tables, Reservation
from django.db import transaction


class TablesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tables
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):

    reservation_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Reservation
        fields = '__all__'

    @transaction.atomic
    def create(self, validated_data):
        table = validated_data['table_id']
        if table.busyness:
            raise serializers.ValidationError({"table_id": "Этот столик уже занят."})

        validated_data['table_id'].busyness = True
        validated_data['table_id'].save()

        reservation = Reservation.objects.create(**validated_data)
        return reservation

    def validate_reservation_time(self, value):
        """
        Проверяет, что дата и время бронирования не раньше текущего момента и не менее чем через 5 минут от текущего момента.
        """
        now = timezone.localtime(timezone.now())
        min_reservation_time = now + datetime.timedelta(minutes=5)

        if value < now:
            raise serializers.ValidationError("Дата и время бронирования не могут быть в прошлом.")
        if value < min_reservation_time:
            raise serializers.ValidationError("Дата и время бронирования должны быть не менее чем через 5 минут от текущего момента.")
        return value