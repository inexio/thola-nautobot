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
    path("tholadevice/<uuid:pk>/status/", views.TholaDeviceStatusView.as_view(), name="tholadevice_status"),

    # THOLA onboarding
    path("onboarding/", views.TholaOnboardingListView.as_view(), name="tholaonboarding_list"),
    path("onboarding/add/", views.TholaOnboardingEditView.as_view(), name="tholaonboarding_add"),
    path("onboarding/<uuid:pk>/", views.TholaOnboardingView.as_view(), name="tholaonboarding"),
    path("onboarding/<uuid:pk>/edit/", views.TholaOnboardingEditView.as_view(), name="tholaonboarding_edit"),
    path("onboarding/<uuid:pk>/delete/", views.TholaOnboardingDeleteView.as_view(), name="tholaonboarding_delete")
]
