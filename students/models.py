# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Student(models.Model):
    enrollment_number = models.CharField(max_length=20, blank=False, null=False, primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    session = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    parents_phone_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_on = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('A', 'Absent'),
        ('P', 'Present'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records' , default=1)
    
    date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    teacher_id = models.CharField(max_length=150, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_on = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        formatted_date = self.date.strftime('%d-%m-%y %H:%M')
        return f"{self.student.name} ({self.student.enrollment_number}) - {formatted_date} - {self.status} - Teacher: {self.teacher_id}"

    def formatted_created_on(self):
        return self.created_on.strftime('%d-%m-%y %H:%M') if self.created_on else ''

    def formatted_updated_on(self):
        return self.updated_on.strftime('%d-%m-%y %H:%M') if self.updated_on else ''

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            self.teacher_id = self._get_teacher_username()
        self.updated_on = timezone.now()  # Update the 'updated_on' field before saving
        super(AttendanceRecord, self).save(*args, **kwargs)

    def _get_teacher_username(self):
        try:
            return User.objects.get(username=self.teacher_id).username
        except User.DoesNotExist:
            return None
