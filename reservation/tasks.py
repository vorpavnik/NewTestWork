from celery import shared_task
from django.utils import timezone
from .models import Tables, Reservation
import logging
import datetime

logger = logging.getLogger(__name__)

@shared_task
def update_tables_busyness_task():
    """
    Задача Celery для обновления состояния занятости столиков и статуса бронирований.
    """
    logger.info('Запущено обновление состояния занятости столиков и статуса бронирований')
    now = timezone.localtime(timezone.now())

    occupied_tables = Tables.objects.filter(busyness=True)

    for table in occupied_tables:
        try:
            latest_reservation = Reservation.objects.filter(table_id=table, active=True).order_by(
                '-reservation_time', '-id').first()

            if latest_reservation:
                reservation_end_time = latest_reservation.reservation_time + datetime.timedelta(
                    minutes=latest_reservation.duration_minutes)

                if reservation_end_time <= now:
                    # Освобождаем столик
                    table.busyness = False
                    table.save()
                    logger.info(f"Столик '{table.name}' (ID: {table.id}) освободился.")

                    # Деактивируем бронирование
                    latest_reservation.active = False
                    latest_reservation.save()
                    logger.info(f"Бронирование (ID: {latest_reservation.id}) деактивировано.")
            else:
                # Если нет активных бронирований для столика, снимаем отметку о занятости
                table.busyness = False
                table.save()
                logger.info(
                    f"Столик '{table.name}' (ID: {table.id}) был помечен как занятый, но не имеет активных бронирований. Отметка о занятости снята.")

        except Exception as e:
            logger.error(f"Ошибка при обработке столика {table.id}: {e}", exc_info=True)


@shared_task
def delete_old_reservations_task():
    """
    Удаляет записи бронирований старше 3 месяцев из БД.
    """
    logging.info('Запущено удаление старых бронирований из БД')
    now = timezone.localtime(timezone.now())
    cutoff_date = now - datetime.timedelta(days=90)  # 3 месяца = 90 дней

    # Найти бронирования, у которых reservation_time меньше или равно cutoff_date
    old_reservations = Reservation.objects.filter(reservation_time__lte=cutoff_date)

    deleted_count = old_reservations.delete()[0]  # Удалить бронирования и получить количество удаленных записей

    logger.info(f"Удалено {deleted_count} старых бронирований.")