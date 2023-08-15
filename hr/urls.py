from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', loginpage, name='login'),
    path('index/', index, name='index'),
    path('logout/',logoutpage ,name='logout'),
    path('my_profile/',my_profile,name='my_profile'),
    path('view_all_employee/',view_all_employee,name='view_all_employee'),
    path('deactivate_employee_/<int:id>/', deactivate_employee, name='deactivate_employee'),
    path('update_employee/<int:id>',update_employee,name="update_employee"),
    path('add_department/',add_department,name='add_department'),
    path('view_department/',view_department,name='view_department'),
    path('fill_attendance/',fill_attendance,name='fill_attendance'),
    path('attendence_request/',attendence_request,name='attendence_request'),
    path('view_attendence_requests/',view_attendence_requests,name='view_attendence_requests'),
    path('view_attendences/', view_attendences, name='view_attendences'),
    path('download_attendance_csv/', download_attendance_csv, name='download_attendance_csv_default'),
    path('add_employee/', add_employee, name='add_employee'),
    path('download_attendance_csv/<str:start_date>/<str:end_date>/', download_attendance_csv, name='download_attendance_csv'),
    path('change_password/', change_password, name='change_password'),
    path('accept-reject-attendance/<int:attendance_id>/<str:action>/', accept_reject_attendance, name='accept_reject_attendance'),
    path('leave_application/',leave_application,name='leave_application'),
    path('view_all_leaves/',view_all_leaves,name='view_all_leaves'),
    path('approve_leave/<int:id>/<str:action>/', approve_leave, name='approve_leave'),
    path('track_leave/',track_leave,name='track_leave'),
    path('cancel_leave/<int:id>/', cancel_leave, name='cancel_leave'),
    path('show_attendence_graph', show_attendence_graph, name='show_attendence_graph'),


]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)