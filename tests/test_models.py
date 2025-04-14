import pytest
from django.utils import timezone
from reservation.models import Reservation, Tables

@pytest.mark.django_db
def test_create_reservation():
    """
    Тестирует создание бронирования.
    """
    table = Tables.objects.create(name="Test Table", seats=4, location="indoor", busyness=False)
    reservation = Reservation.objects.create(
        customer_name="Test Customer",
        table_id=table,
        reservation_time=timezone.now() + timezone.timedelta(hours=1),
        duration_minutes=60,
        active=True
    )
    assert Reservation.objects.count() == 1
    assert reservation.customer_name == "Test Customer"

@pytest.mark.django_db
def test_reservation_table_relation():
    """
    Тестирует связь бронирования со столиком.
    """
    table = Tables.objects.create(name="Test Table", seats=4, location="indoor", busyness=False)
    reservation = Reservation.objects.create(
        customer_name="Test Customer",
        table_id=table,
        reservation_time=timezone.now() + timezone.timedelta(hours=1),
        duration_minutes=60,
        active=True
    )
    assert reservation.table_id == table
    assert table.reservation_set.count() == 1