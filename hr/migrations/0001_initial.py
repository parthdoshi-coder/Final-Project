# Generated by Django 3.2.12 on 2023-08-10 06:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('department_name', models.CharField(max_length=50)),
                ('added_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('emp_code', models.CharField(max_length=20, unique=True)),
                ('profile', models.ImageField(blank=True, null=True, upload_to='images')),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(blank=True, max_length=13, null=True)),
                ('date_of_birth', models.DateField()),
                ('employee_address', models.TextField(max_length=1000)),
                ('aadhar_number', models.CharField(blank=True, max_length=12, null=True, unique=True)),
                ('pan_number', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('date_of_joining', models.DateField()),
                ('is_hr', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('city_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.city')),
                ('dep_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.department')),
                ('designation_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.designation')),
            ],
        ),
        migrations.CreateModel(
            name='Leavetype',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Leaves',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('fro', models.DateField(null=True)),
                ('to', models.DateField(null=True)),
                ('num_of_days', models.FloatField(default=0)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('description', models.TextField(null=True)),
                ('emp_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
                ('leavetype_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hr.leavetype')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='state_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.state'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('att_date', models.DateField()),
                ('in_time', models.TimeField()),
                ('out_time', models.TimeField(blank=True, null=True)),
                ('emp_id', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='hr.employee')),
            ],
        ),
    ]
