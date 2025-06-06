from django.urls import path
#from . import views
from accounting.views import expense_views
from accounting.views import collection_views

app_name = "accounting"

urlpatterns = [
    path('', expense_views.accounting_index, name='index'),
    
    # 経費申請機能
    path("apply/", expense_views.expense_apply, name="expense_apply"),
    path("list/", expense_views.expense_list, name="expense_list"),
    path("detail/<int:id>/", expense_views.expense_detail, name="expense_detail"),
    path('update/<int:id>/', expense_views.expense_update, name='expense_update'),
    path('delete/<int:id>/', expense_views.expense_delete, name='expense_delete'),
    
    # 徴収機能
    path('collection/create/', collection_views.collection_create, name='collection_create'),
    path('collection/<int:year>/', collection_views.collection_list, name='collection_list'),
    path('collection/<int:year>/<int:pk>/', collection_views.collection_detail, name='collection_detail'),
    path('collection/<int:pk>/update/', collection_views.collection_update, name='collection_update'),
    path('collection/<int:pk>/delete/', collection_views.collection_delete, name='collection_delete'),
]