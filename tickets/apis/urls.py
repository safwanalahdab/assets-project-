from django.urls import path

from .views import (
    ticket_list_create_api,
    ticket_detail_update_delete_api,
    ticket_comments_list_create_api,
)

urlpatterns = [
    path("", ticket_list_create_api, name="ticket-list-create"),
    path("<int:pk>/", ticket_detail_update_delete_api, name="ticket-detail"),
    path(
        "<int:pk>/comments/",
        ticket_comments_list_create_api,
        name="ticket-comments",
    ),
]
