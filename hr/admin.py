from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Designation)
admin.site.register(City)
admin.site.register(State)
admin.site.register(Employee)
admin.site.register(Department)
admin.site.register(Leavetype)
admin.site.register(Leaves)
admin.site.register(Attendance)
admin.site.register(RequestedAttendance)