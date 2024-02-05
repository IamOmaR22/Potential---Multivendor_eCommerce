from django.core.management.base import BaseCommand
from django.utils import timezone
from ecom_app.models import Order, DailyData

class Command(BaseCommand):
    help = 'Calculate and save daily revenue data'

    def handle(self, *args, **options):
        today = timezone.now().date()
        orders_today = Order.objects.filter(created_at__date=today)
        total_revenue = sum(order.total_amount for order in orders_today)

        DailyData.objects.create(date=today, total_revenue=total_revenue)

        self.stdout.write(self.style.SUCCESS('Daily revenue data saved successfully.'))