from django.contrib import admin
from .models import RequestLog, Task, BlockedIP

# Register your models here.
admin.site.register(RequestLog)
admin.site.register(Task)
admin.site.register(BlockedIP)