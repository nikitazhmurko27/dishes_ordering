import os
from dishes_ordering.settings import BASE_DIR
from celery import shared_task
import csv
from dishes.views import get_daily_orders


@shared_task
def collect_daily_order_to_csv():
    header = ['dish', 'is_change', 'difference']
    data = get_daily_orders()

    if not os.path.exists(BASE_DIR / 'reports'):
        os.mkdir(BASE_DIR / 'reports')

    with open(BASE_DIR / 'reports/daily_orders_report.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
    return True
