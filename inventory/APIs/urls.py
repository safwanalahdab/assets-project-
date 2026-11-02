from django.urls import path 
from .views import asset_list_create_api,asset_detail_api

urlpatterns = [
    path("assets/",asset_list_create_api,name="asset-list-create"),
    path("assets/<int:pk>/",asset_detail_api,name="asset-list-update"),
]
