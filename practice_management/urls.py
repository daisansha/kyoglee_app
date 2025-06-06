# practice_management/urls.py

from django.urls import path
from . import views

app_name = 'practice_management'

urlpatterns = [
    path('', views.practice_index, name='practice_index'),
    path('create/', views.create_practice_record, name='create_practice_record'),
    path('<int:year>/<int:month>/', views.practice_record, name='practice_record'),
    path('<int:year>/<int:month>/<int:day>/', views.practice_record_detail, name='practice_record_detail'),
    path('<int:year>/<int:month>/delete/', views.delete_practice_month, name='delete_practice_month'),
]
