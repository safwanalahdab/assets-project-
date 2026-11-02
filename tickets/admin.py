from django.contrib import admin
from .models import Tag , Ticket , TicketComment
# Register your models here.

admin.site.register(Tag)
admin.site.register(Ticket)
admin.site.register(TicketComment)


