"""Urls for thola nautobot."""
from . import views
from django.urls import path

app_name = "thola"

urlpatterns = [
    # THOLA device
    path("tholadevice/", views.TholaDeviceListView.as_view(), name="tholadevice_list"),
    path("tholadevice/add/", views.TholaDeviceEditView.as_view(), name="tholadevice_add"),
    path("tholadevice/<uuid:pk>/", views.TholaDeviceView.as_view(), name="tholadevice"),
    path("tholadevice/<uuid:pk>/edit/", views.TholaDeviceEditView.as_view(), name="tholadevice_edit"),
    path("tholadevice/<uuid:pk>/delete/", views.TholaDeviceDeleteView.as_view(), name="tholadevice_delete"),
    path("tholadevice/<uuid:pk>/status/", views.TholaDeviceStatusView.as_view(), name="tholadevice_status")
]
