from django.urls import path
from . import views

urlpatterns = [
    # Vendor URLs
    path('api/vendors/', views.VendorListCreateView.as_view(), name='vendor_list_create'),
    path('api/vendors/<int:pk>/', views.VendorRetrieveUpdateDestroyView.as_view(), name='vendor_detail'),

    path('api/purchase_orders/', views.PurchaseOrderListCreateView.as_view(), name='purchase_order_list_create'),
    path('api/purchase_orders/<int:pk>/', views.PurchaseOrderRetrieveUpdateDestroyView.as_view(), name='purchase_order_detail'),

    path('api/vendors/<int:vendor_id>/performance/', views.VendorPerformanceView.as_view(), name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),

]
