# students/forms.py

from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    DEPARTMENT_CHOICES = [
        ('BCA', 'BCA'),
        ('BJMC', 'BJMC'),
        ('BBA', 'BBA'),
        ('MBA', 'MBA'),
    ]
    
    SESSION_CHOICES = [
        ('2021-24', '2021-24'),
        ('2022-25', '2022-25'),
        ('2023-26', '2023-26'),
    ]

    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    session = forms.ChoiceField(choices=SESSION_CHOICES)

    class Meta:
        model = Student
        fields = '__all__'  # You can specify the fields you want to display here
