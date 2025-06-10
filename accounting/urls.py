from django.urls import path

# 経費申請用ビュー、徴収用ビュー、入出金管理用ビューをインポート
from accounting.views import expense_views
from accounting.views import collection_views
from accounting.views import cash_views

# アプリケーション名を指定（テンプレート内で名前空間付きでURLを参照できる）
# 例：{% url 'accounting:expense_apply' %}
app_name = "accounting"  # URL逆引き用名前空間

# ===============================
# AccountingアプリのURLパターン一覧
# ===============================
# 各URLがどのビュー関数に対応するかを定義

urlpatterns = [
    # 会計メニューなどのトップページ（必要に応じてダッシュボード的に使用）
    path('', expense_views.accounting_index, name='index'),

    # --- 経費申請機能（expense） ---
    path("apply/", expense_views.expense_apply, name="expense_apply"),  # 新規申請
    path("list/", expense_views.expense_list, name="expense_list"),      # 申請一覧
    path("detail/<int:id>/", expense_views.expense_detail, name="expense_detail"),  # 詳細表示
    path('update/<int:id>/', expense_views.expense_update, name='expense_update'),  # 更新
    path('delete/<int:id>/', expense_views.expense_delete, name='expense_delete'),  # 削除

    # --- 徴収機能（collection） ---
    path('collection/create/', collection_views.collection_create, name='collection_create'),  # 新規徴収項目
    path('collection/<int:year>/', collection_views.collection_list, name='collection_list'),  # 年ごとの徴収一覧
    path('collection/<int:year>/<int:pk>/', collection_views.collection_detail, name='collection_detail'),  # 詳細
    path('collection/<int:pk>/update/', collection_views.collection_update, name='collection_update'),      # 更新
    path('collection/<int:pk>/delete/', collection_views.collection_delete, name='collection_delete'),      # 削除
    
    # --- 入出金管理機能（cash） ---
    path('cash/create/', cash_views.cash_page_create, name='cash_page_create'),
    path('cash/list/', cash_views.cash_page_list, name='cash_page_list'),
    path("cash/<uuid:pk>/", cash_views.cash_page, name="cash_page"),
    path("cash/<uuid:pk>/update/", cash_views.cash_plan_update, name="cash_plan_update"),
    path("cash/<uuid:pk>/item/add/", cash_views.cash_item_add, name="cash_item_add"),
    path("cash/<uuid:pk>/item/<int:item_id>/", cash_views.cash_item_detail, name="cash_item_detail"),
    path("cash/<uuid:pk>/item/<int:item_id>/delete/", cash_views.cash_item_delete, name="cash_item_delete"),
    path("cash/<uuid:pk>/delete/", cash_views.cash_page_delete, name="cash_page_delete"),
]