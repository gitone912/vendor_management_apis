from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .helper import *
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import PurchaseOrder


class VendorListCreateView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderListCreateView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer



@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    if instance.status == 'completed' or instance.acknowledgment_date:
        # Get the vendor
        vendor = instance.vendor
        
        # Calculate and update on-time delivery rate
        vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
        
        # Calculate and update quality rating average
        vendor.quality_rating_avg = calculate_quality_rating_avg(vendor)
        
        # Calculate and update average response time
        vendor.average_response_time = calculate_average_response_time(vendor)
        
        # Calculate and update fulfillment rate
        vendor.fulfillment_rate = calculate_fulfillment_rate(vendor)
        
        # Save the vendor model
        vendor.save()
        
class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            data = {
                "on_time_delivery_rate": vendor.on_time_delivery_rate,
                "quality_rating_avg": vendor.quality_rating_avg,
                "average_response_time": vendor.average_response_time,
                "fulfillment_rate": vendor.fulfillment_rate
            }
            return Response(data)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=404)
        
        
@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    try:
        # Retrieve the purchase order
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
        
        # Update acknowledgment_date
        purchase_order.acknowledgment_date = request.data.get('acknowledgment_date')
        purchase_order.save()
        
        # Trigger performance metric recalculation for the vendor
        update_vendor_performance(sender=PurchaseOrder, instance=purchase_order, created=False)
        
        return Response({"message": "Acknowledgment date updated and performance metrics recalculated."}, status=status.HTTP_200_OK)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)