from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'add-every-60-seconds': {
        'task': 'reservation.tasks.update_tables_busyness_task',
        'schedule': 60.0,
        'args': ()
    },
    'add-every-morning': {
        'task': 'reservation.tasks.delete_old_reservations_task',
        'schedule': crontab(hour=9, minute=45),
        'args': ()
    },
}