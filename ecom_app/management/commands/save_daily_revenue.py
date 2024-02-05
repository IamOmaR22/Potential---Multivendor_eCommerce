from django.core.management.base import BaseCommand
from django.utils import timezone
from ecom_app.models import DailyData, Order
from django.db import models

class Command(BaseCommand):
    help = 'Save daily revenue data based on orders'

    def handle(self, *args, **options):
        today = timezone.now().date()

        total_revenue = Order.objects.filter(created_at__date=today).aggregate(total_revenue=models.Sum('total_amount'))['total_revenue'] or 0

        daily_data, created = DailyData.objects.get_or_create(date=today, defaults={'total_revenue': total_revenue})

        if not created:
            daily_data.total_revenue = total_revenue
            daily_data.save()

        self.stdout.write(self.style.SUCCESS('Daily revenue data saved successfully.'))
