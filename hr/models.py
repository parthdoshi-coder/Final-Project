from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    department_name = models.CharField(max_length=50)
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.department_name


class Designation(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


EMP_TYPE_CHOICES = [
    ('Full-time', 'full-time'), ('Part-time', 'part-time'), ('Casual', 'casual'),
    ('Trainee', 'trainee'), ('Probation', 'probation'), ('Comission', 'comission'),
]


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    emp_code = models.CharField(unique=True, max_length=20)  # emp id for login
    profile = models.ImageField(upload_to="images", blank=True, null=True)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=13, null=True, blank=True)
    date_of_birth = models.DateField()
    employee_address = models.TextField(max_length=1000)
    city_id = models.ForeignKey(
        City, null=True, blank=True, on_delete=models.CASCADE)
    state_id = models.ForeignKey(
        State, null=True, blank=True, on_delete=models.CASCADE)
    aadhar_number = models.CharField(
        max_length=12, null=True, blank=True, unique=True)
    pan_number = models.CharField(
        max_length=10, null=True, blank=True, unique=True)
    dep_id = models.ForeignKey(
        Department, null=True, blank=True, on_delete=models.CASCADE)
    designation_id = models.ForeignKey(
        Designation, null=True, blank=True, on_delete=models.CASCADE)
    date_of_joining = models.DateField()
    is_hr = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    def __str__(self):
        return self.emp_code


class Leavetype(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Leaves(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    leavetype_id = models.ForeignKey(
        Leavetype, on_delete=models.CASCADE, default=None)
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, default=None)
    fro = models.DateField(null=True)
    to = models.DateField(null=True)
    num_of_days = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), (
        'cancel', 'Cancel'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    description = models.TextField(null=True)

    def __str__(self):
        return self.emp_id.user.username


class Attendance(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, default=None)
    att_date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.emp_id.user.username


class RequestedAttendance(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    emp_id = models.ForeignKey(
        Employee, on_delete=models.CASCADE, default=None)
    att_date = models.DateField()
    in_time = models.TimeField()
    out_time = models.TimeField(null=True, blank=True)
    request_type = models.CharField(max_length=10, choices=[(
        'new', 'New Request'), ('change', 'Change Request')], default='new')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), (
        'approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    note = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.emp_id.user.username
