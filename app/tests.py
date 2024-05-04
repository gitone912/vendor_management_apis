from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Vendor, PurchaseOrder
from datetime import datetime, timedelta

class VendorManagementSystemAPITests(APITestCase):
    def setUp(self):
        # Create a sample vendor
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="Test Contact Details",
            address="Test Address",
            vendor_code="TEST123"
        )

        # Create a sample purchase order
        self.po = PurchaseOrder.objects.create(
            po_number="PO12345",
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=5),
            items=[{"name": "Item 1", "quantity": 5}],
            quantity=5,
            status="pending",
            issue_date=datetime.now()
        )
    
    def test_create_vendor(self):
        # Define the URL for creating a vendor
        url = reverse('vendor_list_create')
        
        # Define the request payload
        data = {
            "name": "New Vendor",
            "contact_details": "New Contact Details",
            "address": "New Address",
            "vendor_code": "NEW123"
        }
        
        # Send POST request
        response = self.client.post(url, data, format='json')
        
        # Assert the response status and data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['vendor_code'], data['vendor_code'])

    def test_get_vendor_performance(self):
        # Define the URL for getting vendor performance metrics
        url = reverse('vendor_performance', args=[self.vendor.id])
        
        # Send GET request
        response = self.client.get(url)
        
        # Assert the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that the response contains the expected fields
        self.assertIn('on_time_delivery_rate', response.data)
        self.assertIn('quality_rating_avg', response.data)
        self.assertIn('average_response_time', response.data)
        self.assertIn('fulfillment_rate', response.data)

    def test_acknowledge_purchase_order(self):
        # Define the URL for acknowledging a purchase order
        url = reverse('acknowledge_purchase_order', args=[self.po.id])
        
        # Define the request payload
        data = {
            "acknowledgment_date": datetime.now().isoformat()
        }
        
        # Send POST request
        response = self.client.post(url, data, format='json')
        
        # Assert the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the purchase order instance
        self.po.refresh_from_db()
        
        # Check that the acknowledgment_date was updated
        self.assertIsNotNone(self.po.acknowledgment_date)
        
        # Verify vendor performance metrics were updated
        self.vendor.refresh_from_db()
        self.assertGreater(self.vendor.average_response_time, 0)

    def test_update_purchase_order_status_to_completed(self):
        # Update purchase order status to completed
        self.po.quality_rating = 4.5
        self.po.status = "completed"
        self.po.delivery_date = datetime.now()
        self.po.save()
        
        # Refresh the vendor instance
        self.vendor.refresh_from_db()
        
        # Assert that the vendor's performance metrics have been updated
        self.assertGreater(self.vendor.on_time_delivery_rate, 0)
        self.assertGreater(self.vendor.quality_rating_avg, 0)
        self.assertGreater(self.vendor.fulfillment_rate, 0)

    def test_delete_vendor(self):
        # Define the URL for deleting a vendor
        url = reverse('vendor_detail', args=[self.vendor.id])
        
        # Send DELETE request
        response = self.client.delete(url)
        
        # Assert the response status
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the vendor has been deleted
        with self.assertRaises(Vendor.DoesNotExist):
            Vendor.objects.get(id=self.vendor.id)
