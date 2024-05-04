from django.db.models import Avg, Count, Q, F
from .models import PurchaseOrder, Vendor

def calculate_on_time_delivery_rate(vendor):
    # Calculate the number of completed POs delivered on or before delivery_date
    on_time_deliveries = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        delivery_date__gte=F('order_date'),
        delivery_date__lte=F('delivery_date')
    ).count()

    # Calculate the total number of completed POs for the vendor
    total_completed_pos = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed'
    ).count()

    # Calculate on-time delivery rate
    if total_completed_pos > 0:
        return (on_time_deliveries / total_completed_pos) * 100
    else:
        return 0.0

def calculate_quality_rating_avg(vendor):
    # Calculate the average quality rating for completed POs
    average_rating = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed',
        quality_rating__isnull=False
    ).aggregate(average=Avg('quality_rating'))

    return average_rating['average'] if average_rating['average'] is not None else 0.0

def calculate_average_response_time(vendor):
    # Calculate the average time difference between issue_date and acknowledgment_date
    completed_pos = PurchaseOrder.objects.filter(
        vendor=vendor,
        acknowledgment_date__isnull=False
    )

    if completed_pos.exists():
        total_time_diff = sum(
            (po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos
        )
        return total_time_diff / len(completed_pos)
    else:
        return 0.0

def calculate_fulfillment_rate(vendor):
    # Calculate the number of successfully fulfilled POs (completed without issues)
    successfully_fulfilled = PurchaseOrder.objects.filter(
        vendor=vendor,
        status='completed'
    ).count()

    # Calculate the total number of POs issued to the vendor
    total_pos_issued = PurchaseOrder.objects.filter(
        vendor=vendor
    ).count()

    # Calculate fulfillment rate
    if total_pos_issued > 0:
        return (successfully_fulfilled / total_pos_issued) * 100
    else:
        return 0.0
