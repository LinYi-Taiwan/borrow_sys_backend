from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(BorrowTime)
class BorrowTimeAdmin(admin.ModelAdmin):
    pass
    # list_display = ('借用空間', '開始時間', '結束時間', '借用人信箱')


admin.site.register(Photo)
admin.site.register(Room)
admin.site.register(Profile)
