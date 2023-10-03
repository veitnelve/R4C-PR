from django.urls import path
from .views import add_robot, download_report


urlpatterns = [path('api/robots/', add_robot),
               path('api/download_report', download_report)
               ]