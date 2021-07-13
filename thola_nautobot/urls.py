"""Urls for thola nautobot."""
from . import views
from django.urls import path

app_name = "thola"

urlpatterns = [
    # THOLA config
    path("config/", views.TholaConfigListView.as_view(), name="tholaconfig_list"),
    path("config/add/", views.TholaConfigEditView.as_view(), name="tholaconfig_add"),
    path("config/delete/", views.TholaConfigBulkDeleteView.as_view(), name="tholaconfig_bulkdelete"),
    path("config/<uuid:pk>/", views.TholaConfigView.as_view(), name="tholaconfig"),
    path("config/<uuid:pk>/edit/", views.TholaConfigEditView.as_view(), name="tholaconfig_edit"),
    path("config/<uuid:pk>/delete/", views.TholaConfigDeleteView.as_view(), name="tholaconfig_delete"),
    path("config/<uuid:pk>/status/", views.TholaConfigStatusView.as_view(), name="tholaconfig_status"),

    # THOLA onboarding
    path("onboarding/", views.TholaOnboardingListView.as_view(), name="tholaonboarding_list"),
    path("onboarding/add/", views.TholaOnboardingEditView.as_view(), name="tholaonboarding_add"),
    path("onboarding/delete/", views.TholaOnboardingBulkDeleteView.as_view(), name="tholaonboarding_bulkdelete"),
    path("onboarding/<uuid:pk>/", views.TholaOnboardingView.as_view(), name="tholaonboarding"),
    path("onboarding/<uuid:pk>/edit/", views.TholaOnboardingEditView.as_view(), name="tholaonboarding_edit"),
    path("onboarding/<uuid:pk>/delete/", views.TholaOnboardingDeleteView.as_view(), name="tholaonboarding_delete")
]
