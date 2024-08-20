from django.db import models
from django.contrib.auth.models import User  # Import the User model for teachers

class Student(models.Model):
    enrollment_number = models.CharField(max_length=20, blank=False, null=False)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    session = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)
    parents_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class AttendanceRecord(models.Model):
    student_name = models.CharField(max_length=100, blank=False, default='')
    student_enrollment_number = models.CharField(max_length=20, blank=False, null=False, default=0)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=[('A', 'Absent'), ('P', 'Present')])
    teacher_id = models.CharField(max_length=150)  # Change to a CharField to store the username

    def __str__(self):
        return f"{self.student_name} ({self.student_enrollment_number}) - {self.date} - {self.status} - Teacher: {self.teacher_id}"

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            self.teacher_id = self._get_teacher_username()
        super(AttendanceRecord, self).save(*args, **kwargs)

    def _get_teacher_username(self):
        if self._state.adding:
            return User.objects.get(username=self.teacher_id).username
        return self.teacher_id
