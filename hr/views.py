import csv
import datetime
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
import plotly.graph_objs as go

# Create your views here.

@csrf_protect
def loginpage(request):

    if request.session.get('username'):

        user = User.objects.filter(username=request.session.get('username'))
        emp_id = Employee.objects.filter(user=user.first()).first()
        context = {
            'username': request.session.get('username'),
            'emp': emp_id,
            'is_hr': emp_id.is_hr
        }
        return render(request, 'index.html', context)
    else:
        if request.method == 'POST':
            username = request.POST.get('uname')
            password = request.POST.get('pass')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                request.session['username'] = username
                return render(request, 'index.html')
            else:
                # return HttpResponse("plese Enter correct password")
                messages.warning(request, 'Invalid login credentials')
        return render(request, 'login.html')

def logoutpage(request):
    # Remove the 'username' from the session
    if 'username' in request.session:
        del request.session['username']
    
    logout(request)
    
    return redirect('login')

@csrf_protect
def add_employee(request):
    if request.method=='POST':
        data = request.POST
        print(request.FILES)
        profile = request.FILES.get('profile')
        profile = request.FILES.get('profile')
        emp_code = request.POST.get('user')
        department=request.POST.get('Department')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        mobile_number=request.POST.get('mobile_number')
        email=request.POST.get('email')
        dob=request.POST.get('dob')
        employee_address=request.POST.get('employee_address')
        state=request.POST.get('state')
        city=request.POST.get('city')
        aadhar_number=request.POST.get('aadhar_number')
        pan_number=request.POST.get('pan_number')
        emp_designation=request.POST.get('designation')
        date_of_joining=request.POST.get('date_of_joining')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        
        try:
            if password != cpassword:
                    return JsonResponse({
                    "message" : "Password and Confirm Password Does not match"
                    })
                
                
            if state:
                state_id = State.objects.get(name=state)
                    
            if city:
                city_id = City.objects.get(name=city)

            if department:
                dep_id = Department.objects.get(department_name=department)

            if emp_designation:
                designation_id = Designation.objects.get(name=emp_designation)

            user_id = User.objects.create(username=emp_code,first_name=first_name, last_name=last_name, email=email)
            user_id.set_password(password)
            user_id.save()
            
            emp_id = Employee.objects.create(user=user_id,emp_code=emp_code,profile=profile, email=email, mobile_number=mobile_number,
                                             date_of_birth=dob, employee_address=employee_address, city_id=city_id,
                                            state_id=state_id, aadhar_number=aadhar_number, pan_number=pan_number, dep_id=dep_id,
                                            designation_id=designation_id, date_of_joining=date_of_joining, is_employee=True,)
            return render(request,'index.html')


        except Exception as e:
                # transaction.set_rollback(True)
                return JsonResponse(  {
                    'error_msg': str(e), 
                    'status_code': 400
                })

    cities =  City.objects.all()
    states = State.objects.all()
    deps = Department.objects.all()
    designation = Designation.objects.all()
            # print(cities)
    context = {
        'cities': cities,
        'states': states,
        'deps': deps,
        'designation': designation 
    }

    return render(request,'add_employee.html', context)

def my_profile(request):
    if request.session.get('username'):
        user = User.objects.filter(username=request.session.get('username'))
        emp_id = Employee.objects.filter(user=user[0])
        print(emp_id[0].profile)
        context = {
            'username': request.session.get('username'),
            'emp': emp_id[0] 
        }
    else:
        context = {}
        
    return render(request,'my_profile.html',context)

def view_all_employee(request):
    print(request.method)
    if request.method == 'POST':
        dep_name = request.POST.get('dep_filter')
        if dep_name == 'all':
            employess = Employee.objects.all()
        else:
            department = Department.objects.get(department_name=dep_name)
            employess = Employee.objects.filter(dep_id=department)
        context = {
            'employees': employess,
            'departments' : Department.objects.all()
        }
        return render(request,'view_all_employee.html', context)
     
    all_deps = Department.objects.all()
    context = {
        'departments': all_deps,
        'employees': Employee.objects.all()
     }
    return render(request,'view_all_employee.html',context)


def index(request):
    if request.session.get('username'):
        user = User.objects.filter(username=request.session.get('username'))
        emp_id = Employee.objects.filter(user=user.first()).first()
        context = {
            'username': request.session.get('username'),
            'emp': emp_id,
            'is_hr': emp_id.is_hr
        }
        print(context)
    else:
        context = {}
    return render(request,'index.html', context)

    # Remove the 'username' from the session
    if 'username' in request.session:
        del request.session['username']
    
    logout(request)
    
    return redirect('login')


def add_department(request):
    if request.method == 'POST':
        dep_name = request.POST.get('dep_name')
        dep = Department.objects.filter(department_name=dep_name)
        if dep:
            messages.success(request, 'Department Already Exist!')
        else:
            Department.objects.create(department_name=dep_name)
            messages.success(request, 'Department added successfully!')
    return render(request, 'add_department.html')

def view_department(request):
    context = {
        'deps': Department.objects.all()
    }
    return render(request, 'view_department.html', context)




@login_required
@csrf_protect
def fill_attendance(request):
    # Get the user object
    user = request.user

    # Initialize context with username
    context = {'username': user.username}

    # Get the employee object
    emp = Employee.objects.filter(user=user).first()

    if emp:
        # Check if attendance exists for today
        att_obj = Attendance.objects.filter(att_date=datetime.date.today(), emp_id=emp).first()

        if att_obj:
            context['in_time'] = att_obj.in_time
            context['out_time'] = att_obj.out_time

        if request.method == 'POST':
            if 'check_in' in request.POST:
                # Check if user has already checked in for the day
                if att_obj:
                    context['message'] = 'You have already checked in today.'
                else:
                    att_date = datetime.date.today()
                    in_time = time.strftime("%H:%M:%S", time.localtime())
                    att_obj = Attendance.objects.create(emp_id=emp, att_date=att_date, in_time=in_time)
                    context['in_time'] = att_obj.in_time
                    context['message'] = 'Check-in successful.'
                return render(request, 'fill_attendance.html', context)

            if 'check_out' in request.POST:
                # Check if user has already checked out for the day
                if not att_obj:
                    context['message'] = 'You have not checked in yet.'
                elif att_obj.out_time:
                    context['message'] = 'You have already checked out today.'
                else:
                    att_obj.out_time = time.strftime("%H:%M:%S", time.localtime())
                    att_obj.save()
                    context['in_time'] = att_obj.in_time
                    context['out_time'] = att_obj.out_time
                    context['message'] = 'Check-out successful.'
                return render(request, 'fill_attendance.html', context)

    # Return the rendered template with context
    return render(request, 'fill_attendance.html', context)

@login_required
@csrf_protect
def attendence_request(request):
    if request.method == 'POST':
        user = request.user
        emp = Employee.objects.filter(user=user).first()
        
        RequestedAttendance.objects.create(
            emp_id=emp, att_date=request.POST.get('att_date'), in_time=request.POST.get('intime'),
            out_time=request.POST.get('outtime'), request_type=request.POST.get('request_type'),
            status='pending', note=request.POST.get('note')             
        )
        return render(request, 'attendence_request.html')
    return render(request, 'attendence_request.html')

@login_required
def view_attendence_requests(request):
    all_requests = RequestedAttendance.objects.filter(status='pending')
    return render(request, 'view_attendence_request.html', context={'attendance_records': all_requests})

@login_required
def accept_reject_attendance(request, attendance_id, action):
    attendence = get_object_or_404(RequestedAttendance, id=attendance_id)
    if attendence:
        if action=='approve' and attendence.request_type == 'new':
            att_obj = Attendance.objects.filter(att_date=attendence.att_date, emp_id=attendence.emp_id).first()
            if not att_obj:
                Attendance.objects.create(emp_id=attendence.emp_id, att_date=attendence.att_date,
                                        in_time=attendence.in_time, out_time=attendence.out_time)
                attendence.status = 'approved' 
            else:
                return HttpResponse(f"Already have attendence for date {attendence.att_date} either you can create a change request")    
            
        elif action=='approve' and attendence.request_type == 'change':
            att_obj = Attendance.objects.filter(att_date=attendence.att_date, emp_id=attendence.emp_id).first()
            if att_obj:
                att_obj.in_time = attendence.in_time
                att_obj.out_time = attendence.out_time
                att_obj.save()
                attendence.status = 'approved'  
            else:
                return HttpResponse("No Record Found for selected date")  
        
        elif action=='reject':
            attendence.status = 'rejected'
    
    attendence.save()
    all_requests = RequestedAttendance.objects.filter(status='pending')
    return render(request, 'view_attendence_request.html', context={'attendance_records': all_requests})
            
@login_required
def view_attendences(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    employee = request.GET.get('employee')
    all_emp = Employee.objects.all()
    
    user = request.user
    emp = Employee.objects.filter(user=user).first()
    
    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        
        if employee and emp.is_hr:
            selected_emp = get_object_or_404(Employee, emp_code = employee)
            if selected_emp:
                attendances = Attendance.objects.filter(emp_id=selected_emp, att_date__range=(start_date, end_date))
            else:
                attendances = Attendance.objects.filter(att_date__range=(start_date, end_date))
        else:
            attendances = Attendance.objects.filter(emp_id=emp, att_date__range=(start_date, end_date))

        context = {
            'attendances': attendances,
            'start_date': start_date,
            'end_date': end_date,
            'is_hr': emp.is_hr,
            'all_emp': all_emp, 
        }

        return render(request, 'view_attendences.html', context)
    
    return render(request, 'view_attendences.html', {
        'start_date': None,
        'end_date': None,
        'all_emp': all_emp, 
        'is_hr': emp.is_hr
    })

@login_required
def download_attendance_csv(request, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    user = request.user
    emp = Employee.objects.filter(user=user).first()

    attendances = Attendance.objects.filter(emp_id=emp, att_date__range=(start_date, end_date))

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_report_{emp}.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'In Time', 'Out Time'])  # Add more headers as needed

    for attendance in attendances:
        writer.writerow([attendance.att_date, attendance.in_time, attendance.out_time])

    return response

@login_required
def leave_application(request):
    leavetype = Leavetype.objects.all()

    if request.method == "POST":
        fro = request.POST.get('start_date') 
        to = request.POST.get('end_date')
        leave_type = request.POST.get('leave_type')
        description = request.POST.get('description')
        
        # Convert the date strings to datetime objects
        fro_date = datetime.datetime.strptime(fro, '%Y-%m-%d')
        to_date = datetime.datetime.strptime(to, '%Y-%m-%d')
        
        user = User.objects.filter(username=request.session.get('username')).first()
        emp_id = Employee.objects.filter(user=user).first()
        
        # Check if there's an overlapping leave for the same user and date range
        overlapping_leave = Leaves.objects.filter(emp_id=emp_id, fro__lte=to_date, to__gte=fro_date, status__in=['pending', 'approved']).first()

        if overlapping_leave:
            messages.error(request, "You have already applied for leave on overlapping dates.")
        else:
            if leave_type:
                leavetype_id = Leavetype.objects.filter(name=leave_type).first()
                
                leave = Leaves.objects.create(emp_id=emp_id, fro=fro, to=to, leavetype_id=leavetype_id,
                                              description=description)

                num_of_days = (to_date - fro_date).days
                leave.num_of_days = num_of_days + 1
                leave.save()

                messages.success(request, f"You have successfully applied for {num_of_days + 1} days leave.")
                
            else:
                messages.error(request, "Leave type is required.")
        
        return render(request, 'leave_application.html', {'leavetype': leavetype})
    
    context = {
        'leavetype': leavetype 
    }

    return render(request, 'leave_application.html', context)

@login_required
def view_all_leaves(request):
    employee = request.GET.get('employee')
    emp_id = Employee.objects.filter(emp_code=employee).first()

    status = request.GET.get('status')
    leave_records = Leaves.objects.select_related('leavetype_id', 'emp_id')

    if employee and status:
        leave_records = leave_records.filter(emp_id=emp_id, status=status)

    elif employee:
        leave_records = leave_records.filter(emp_id=emp_id)

    elif status:
        leave_records = leave_records.filter(status=status)

    context = {
        'leave_records': leave_records,
        'all_emp': Employee.objects.all()
    }

    return render(request, 'view_all_leaves.html', context)

def approve_leave(request, id, action):

    leave_records = Leaves.objects.select_related('leavetype_id', 'emp_id').all()

    context = {
        'leave_records': leave_records,
        'all_emp': Employee.objects.all()
    }
    leave = Leaves.objects.get(id=id)
    
    if action == 'accept':
        leave.status = 'approved'
        leave.save()   
        return render(request,'view_all_leaves.html', context)
    
    elif action == 'reject':
        leave.status = 'rejected'
        leave.save()
        return render(request,'view_all_leaves.html', context)  

def track_leave(request):
    user = User.objects.filter(username=request.session.get('username')).first()
    emp_id = Employee.objects.filter(user=user).first()
    leave_records = Leaves.objects.filter(emp_id=emp_id).exclude(status='cancel')

    context = {
        'leave_records': leave_records,
        'all_emp': Employee.objects.all()
    }
    return render(request,'track_leave.html',context)

def cancel_leave(request, id):
    leave = get_object_or_404(Leaves, id=id)
    user = User.objects.filter(username=request.session.get('username')).first()
    emp_id = Employee.objects.filter(user=user).first()
    leave_records = Leaves.objects.filter(emp_id=emp_id, status='cancel')
    
    context = {
        'leave_records': leave_records
    }
    
    if leave.status == 'pending':
        leave.status = 'cancel'
        leave.save()
        # Add a success message
        messages.success(request, "The leave has been cancelled.")
    else:
        # Add an error message
        messages.error(request, "The leave cannot be cancelled as it is not in pending status.")
    
    return render(request, 'track_leave.html', context)


def deactivate_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('view_all_employee')  # Redirect to the employee list page
    
    context = {
        'employee': employee
    }
    return render(request, 'deactivate_employee.html', context)

def update_employee(request,id):
    print(request.POST)
    employee = Employee.objects.get(id = id)
    #  context = {'Employee' : queryset}
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=id)
        # new_profile = request.FILES.get('profile') 
        # if new_profile:
        #      employee.profile.save(new_profile.name, add_employee(new_profile.read()), save=False)
        
        vals = request.POST
        employee.user.first_name = vals.get('first_name')
        employee.user.last_name = vals.get('last_name')
        employee.mobile_number = vals.get('mobile_number')
        employee.employee_address= vals.get('employee_address')
        employee.state_id = State.objects.filter(name=vals.get('state')).first()
        employee.city_id = City.objects.filter(name=vals.get('city')).first()
        employee.designation_id = Designation.objects.filter(name=vals.get('designation')).first()
        employee.profile = request.FILES.get('profile')



        employee.save()
        
        cities =  City.objects.all()
        states = State.objects.all()
        deps = Department.objects.all()
        designation = Designation.objects.all()
        context = {
            'employee': employee,
            'cities': cities,
            'states': states,
            'deps': deps,
            'designation': designation 
        }
        
        return redirect('view_all_employee')
        
        return render(request,'update_employee.html', context)
    else:
        
        cities =  City.objects.all()
        states = State.objects.all()
        deps = Department.objects.all()
        designation = Designation.objects.all()
        context = {
            'form' : 'form',
            'employee': employee,
            'cities': cities,
            'states': states,
            'deps': deps,
            'designation': designation 
        }

      
        return render(request,'update_employee.html', context)
    
    
def change_password(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    user = request.user
    if request.method == "POST":      
        c = request.POST['currentpassword']  
        n = request.POST['newpassword']    
        try:
            if user.check_password(c):
                user.set_password(n)                
                user.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"         
        return render(request,'change_password.html',locals())

def show_attendence_graph(request):
    
    if request.method == 'GET':
        from datetime import datetime
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        emp_id = get_object_or_404(Employee, emp_code=request.session.get('username'))
        selected_attendences = Attendance.objects.filter(emp_id=emp_id, att_date__range=[start_date, end_date]).values()

        date_working_hours = {}
        for entry in selected_attendences:
            date = entry["att_date"]
            intime = entry["in_time"]
            outtime = entry["out_time"]
            working_hours = (datetime.combine(datetime.today(), outtime) - datetime.combine(datetime.today(), intime)).seconds / 3600

            if date not in date_working_hours:
                date_working_hours[date] = []
            date_working_hours[date].append(working_hours)

        # Calculate average working hours for each date
        average_working_hours = {date: sum(hours) / len(hours) for date, hours in date_working_hours.items()}

        dates = list(average_working_hours.keys())
        averages = list(average_working_hours.values())

        graph_data = [
            go.Bar(x=dates, y=averages, name=f'Average Working Hours for {emp_id}')
        ]
        graph_layout = go.Layout(title=f'Working Hours Analysis for {emp_id}', xaxis=dict(type='date'), yaxis=dict(title='Working Hours (hours)'))

        graph_html = go.Figure(data=graph_data, layout=graph_layout).to_html(full_html=False)

        context = {
            'graph': graph_html
        }

        return render(request, 'show_attendence_graph.html', context)
