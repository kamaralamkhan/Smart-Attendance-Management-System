# views.py

from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from twilio.rest import Client
from students.models import Student, AttendanceRecord
from .forms import StudentForm

def dashboard(request):
    # Your dashboard view logic here
    return render(request, 'dashboard.html')

def send_sms(student_name, parent_phone_number):
    # Your Twilio credentials
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    # Initialize the Twilio client
    client = Client(account_sid, auth_token)

    # Compose the SMS message
    message_body = f"Your ward {student_name} is absent today. Please contact the college for details."

    try:
        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=twilio_phone_number,
            to=parent_phone_number
        )

        # Check the status of the message
        if message.status == 'sent':
            print(f"SMS successfully sent to {parent_phone_number}. Message SID: {message.sid}")
        else:
            print(f"Failed to send SMS. Message SID: {message.sid}, Status: {message.status}")

    except Exception as e:
        print(f"Error sending SMS: {e}")

def student_login(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_login')
    else:
        form = StudentForm()
    return render(request, 'student.html', {'form': form})

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard page
        else:
            error_message = 'Invalid username or password.'
    else:
        error_message = None
    return render(request, 'teacher.html', {'error_message': error_message})

@login_required
def student_list(request):
    department = request.GET.get('department')
    session = request.GET.get('session')
    subject = request.GET.get('subject')

    if department and session:
        students = Student.objects.filter(department=department, session=session)
    else:
        students = []  # Empty queryset when no filter is applied

    if request.method == 'POST':
        student_names = request.POST.getlist('student_name')
        enrollment_numbers = request.POST.getlist('student_enrollment_number')
        attendance_values = request.POST.getlist('attendance_value')
        parent_phone_numbers = request.POST.getlist('parent_phone_number')

        # Get the currently logged-in teacher
        teacher = request.user

        for name, enrollment_number, value, parent_phone_number in zip(
            student_names, enrollment_numbers, attendance_values, parent_phone_numbers
        ):
            try:
                student = Student.objects.get(enrollment_number=enrollment_number)

                # Pass the subject information when creating AttendanceRecord
                AttendanceRecord.objects.create(
                    student=student,
                    status=value,
                    teacher_id=teacher,
                    subject=subject  # Add this line to set the subject
                )

                # If the student is absent, send SMS to the parent
                if value == 'A':
                    send_sms(student.name, parent_phone_number)

            except Student.DoesNotExist:
                # Handle the case where the student is not found
                # You might want to log this or handle it according to your application logic
                pass

    return render(request, 'student_list.html', {'students': students})

def view_attendance(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        session = request.POST.get('session')
        subject = request.POST.get('subject')  # Add this line to get the selected subject

        if department and session:
            students = Student.objects.filter(department=department, session=session)
            attendance_records = AttendanceRecord.objects.filter(student__in=students)
        else:
            students = []
            attendance_records = []

        return render(request, 'view_attendance.html', {'students': students, 'attendance_records': attendance_records, 'selected_subject': subject})

    return render(request, 'view_attendance.html')  # This will render an empty form initially
