from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Max, Q
from django.utils import timezone

from .models import Doctor, Appointment, EmergencyAlert, DoctorNotification, ContactMessage


# =========================
# HOME
# =========================
def home(request):
    doctors = Doctor.objects.select_related("user")[:6]
    return render(request, "home.html", {"doctors": doctors})


# =========================
# DOCTOR LIST
# =========================
from django.shortcuts import render
from django.db.models import Q
from .models import Doctor

def doctor_list(request):
    # 1. Get the 'q' parameter from the URL
    query = request.GET.get('q')
    
    # 2. Start with all doctors
    doctors = Doctor.objects.all()
    
    # 3. If a search query exists, filter the list
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(specialization__icontains=query)
        )
    
    # 4. Return the filtered list to the template
    return render(request, 'doctors/doctor_list.html', {'doctors': doctors})
# =========================
# DOCTOR DETAIL
# =========================
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, "doctors/doctor_detail.html", {"doctor": doctor})


# =========================
# BOOK APPOINTMENT
# =========================
@login_required(login_url="patient_login")
def book_appointment(request, user_id):
    doctor = get_object_or_404(Doctor, user_id=user_id)

    if request.method == "GET":
        return render(request, "doctors/book_appointment.html", {"doctor": doctor})

    today = timezone.now().date()

    last_queue = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today
    ).aggregate(Max("queue_number"))["queue_number__max"]

    next_queue = (last_queue or 0) + 1

    appointment = Appointment.objects.create(
        doctor=doctor,
        patient_name=request.POST.get("patient_name"),
        patient_email=request.user.email,
        patient_phone=request.POST.get("patient_phone"),
        appointment_date=today,
        queue_number=next_queue,
        status="waiting",
    )

    DoctorNotification.objects.create(
        doctor=doctor.user,
        appointment=appointment
    )

    return redirect("appointment_success", appointment_id=appointment.id)


# =========================
# APPOINTMENT SUCCESS
# =========================
def appointment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, "doctors/appointment_success.html", {"appointment": appointment})
from django.contrib.auth.decorators import login_required

@login_required(login_url='patient_login') # Redirects to login if not authenticated
def book_appointment(request, doctor_id):
    # Your booking logic here...
    return render(request, 'booking_form.html')


# =========================
# DOCTOR LOGIN
# =========================
def doctor_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("doctor_dashboard")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user and user.is_staff:
            login(request, user)
            return redirect("doctor_dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "doctors/doctor_login.html")


# =========================
# DOCTOR DASHBOARD
# ======================
@login_required
def doctor_dashboard(request):
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        # If a patient tries to access this, send them back
        messages.error(request, "Access Denied: You do not have a Doctor profile.")
        return redirect('patient_dashboard')

    return render(request, 'doctors/doctor_dashboard.html', {'doctor': doctor})
# =========================
# NEXT PATIENT
# =========================
@login_required(login_url="doctor_login")
def next_patient(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    today = timezone.now().date()

    current = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today,
        status="in_progress"
    ).first()

    if current:
        current.status = "completed"
        current.save()

    next_patient = Appointment.objects.filter(
        doctor=doctor,
        appointment_date=today,
        status="waiting"
    ).order_by("queue_number").first()

    if next_patient:
        next_patient.status = "in_progress"
        next_patient.save()

    return redirect("doctor_dashboard")


# =========================
# MARK COMPLETED
# =========================
@login_required(login_url="doctor_login")
def mark_completed(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)
    appointment.status = "completed"
    appointment.save()

    return redirect("doctor_dashboard")


# =========================
# RESOLVE EMERGENCY
# =========================
@login_required(login_url="doctor_login")
def resolve_emergency(request, emergency_id):
    emergency = get_object_or_404(EmergencyAlert, id=emergency_id, doctor=request.user)
    emergency.status = "resolved"
    emergency.save()
    return redirect("doctor_dashboard")


# =========================
# LOGOUT (COMMON)
# =========================
def logout_view(request):
    logout(request)
    return redirect("home")


# =========================
# PATIENT LOGIN + SIGNUP
# =========================
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def patient_login(request):
    # 1. If user is already logged in, send them to dashboard
    if request.user.is_authenticated:
        return redirect('patient_dashboard')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # --- LOGIN LOGIC ---
        if form_type == "login":
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                # Find user by email first
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('patient_dashboard')
                else:
                    messages.error(request, "Invalid password.")
            except User.DoesNotExist:
                messages.error(request, "No account found with this email.")

        # --- SIGNUP LOGIC ---
        elif form_type == "signup":
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            # Validation: Passwords match
            if password != confirm_password:
                messages.error(request, "Passwords do not match.")
                return redirect("patient_login")

            # Validation: Email exists (This prevents the IntegrityError)
            if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
                messages.error(request, "A user with this email/username already exists.")
                return redirect("patient_login")

            try:
                # Create the user safely
                user = User.objects.create_user(
                    username=email, # Using email as username
                    email=email,
                    password=password,
                    first_name=name
                )
                
                # IMPORTANT: If you have a Patient profile model, create it here:
                # Patient.objects.create(user=user)

                login(request, user)
                messages.success(request, f"Welcome, {name}!")
                return redirect('patient_dashboard')
                
            except Exception as e:
                messages.error(request, "An error occurred during signup. Please try again.")

    return render(request, 'patient_login.html')


# =========================
# PATIENT DASHBOARD
# =========================
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def patient_dashboard(request):
    # Check if the logged-in user is actually a patient
    # This assumes you have a way to identify them (like a group or profile)
    if hasattr(request.user, 'doctor'): 
        messages.error(request, "Access Denied: Doctors cannot access the Patient Dashboard.")
        return redirect('doctor_dashboard')
    
    return render(request, 'patient_dashboard.html')
# views.py
from django.shortcuts import render

def departments_view(request):
    return render(request, 'departments.html')

# =========================
# CANCEL APPOINTMENT
# =========================
@login_required(login_url='patient_login')
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        patient_email=request.user.email
    )
    appointment.status = "cancelled"
    appointment.save()
    return redirect("patient_dashboard")


# =========================
# STATIC PAGES
# =========================
def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            message=request.POST.get("message"),
        )
        messages.success(request, "Message sent!")

    return render(request, "contact.html")

def gallery(request):
    return render(request, 'gallery.html')
@login_required(login_url="doctor_login")
def view_notification_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
    )

    # mark notification as read
    DoctorNotification.objects.filter(
        doctor=request.user,
        appointment=appointment
    ).update(is_read=True)

    return render(
        request,
        "doctors/appointment_detail.html",
        {"appointment": appointment}
    )
def receptionist_login(request):
    if request.user.is_authenticated and request.user.groups.filter(name="Receptionist").exists():
        return redirect("receptionist_dashboard")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user and user.groups.filter(name="Receptionist").exists():
            login(request, user)
            return redirect("receptionist_dashboard")

        messages.error(request, "Invalid receptionist credentials")

    return render(request, "receptionist/login.html")
@login_required(login_url="receptionist_login")
def receptionist_dashboard(request):
    doctors = User.objects.filter(is_staff=True)

    return render(
        request,
        "receptionist/receptionist.html",
        {"doctors": doctors}
    )
@login_required(login_url="receptionist_login")
def receptionist_logout(request):
    logout(request)
    return redirect("home")
from django.db.models import Q

@login_required(login_url="receptionist_login")
def receptionist_appointments(request):

    query = request.GET.get("q", "").strip()

    appointments = Appointment.objects.select_related("doctor__user")

    if query:
        appointments = appointments.filter(
            Q(patient_name__icontains=query) |
            Q(patient_phone__icontains=query) |
            Q(doctor__user__first_name__icontains=query) |
            Q(doctor__user__last_name__icontains=query) |
            Q(doctor__specialization__icontains=query) |
            Q(appointment_date__icontains=query)
        )

    appointments = appointments.order_by("-appointment_date")

    return render(request, "receptionist/appointments.html", {
        "appointments": appointments,
        "query": query
    })
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def delete_all_appointments(request):
    if request.method == "POST":
        Appointment.objects.all().delete()
        messages.success(request, "All appointments deleted successfully!")
        return redirect("receptionist_appointments")
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def delete_selected_appointments(request):
    if request.method == "POST":
        ids = request.POST.getlist("ids")
        Appointment.objects.filter(id__in=ids).delete()
        messages.success(request, "Selected appointments deleted!")
    return redirect("receptionist_appointments")    
    

    return redirect("receptionist_appointments")    
@login_required(login_url="receptionist_login")
def add_appointment(request):
    doctors = User.objects.filter(is_staff=True)

    if request.method == "POST":
        today = timezone.now().date()
        doctor_id = request.POST.get("doctor_id")

        last_queue = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=today
        ).aggregate(Max("queue_number"))["queue_number__max"]

        next_queue = (last_queue or 0) + 1

        Appointment.objects.create(
            doctor_id=doctor_id,
            patient_name=request.POST.get("patient_name"),
            patient_email=request.POST.get("patient_email"),
            patient_phone=request.POST.get("patient_phone"),
            appointment_date=today,
            queue_number=next_queue,
            status="waiting",
        )

        messages.success(request, "Appointment added successfully")
        return redirect("receptionist_appointments")

    return render(request, "receptionist/add_appointment.html", {
        "doctors": doctors
    })
@login_required(login_url="receptionist_login")
def send_emergency(request):
    if request.method == "POST":
        doctor = get_object_or_404(User, id=request.POST.get("doctor_id"))

        EmergencyAlert.objects.create(
            doctor=doctor,
            patient_name="Emergency",
            patient_phone="N/A",
            message="Emergency case"
        )

    return redirect("receptionist_dashboard") 
def book_appointment(request, user_id):
    doctor = get_object_or_404(Doctor, user_id=user_id)

    # ✅ ONLY SHOW FORM
    if request.method == "GET":
        return render(request, "doctors/book_appointment.html", {
            "doctor": doctor
        })

    # ✅ ONLY CREATE ON POST
    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        patient_email = request.POST.get("patient_email")
        patient_phone = request.POST.get("patient_phone")

        # 🚨 SAFETY CHECK
        if not patient_name or not patient_email or not patient_phone:
            messages.error(request, "All fields are required!")
            return redirect("book_appointment", user_id=user_id)

        today = timezone.now().date()

        last_queue = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=today
        ).aggregate(Max("queue_number"))["queue_number__max"]

        next_queue = (last_queue or 0) + 1

        appointment = Appointment.objects.create(
            doctor=doctor,
            patient_name=patient_name,
            patient_email=patient_email,
            patient_phone=patient_phone,
            appointment_date=today,
            queue_number=next_queue,
            status="waiting",
        )

        DoctorNotification.objects.create(
            doctor=doctor.user,
            appointment=appointment
        )

        return redirect("appointment_success", appointment_id=appointment.id)
from django.contrib.auth import logout
from django.shortcuts import redirect

def doctor_logout_view(request):
    logout(request)
    return redirect('home')  # Redirects to home after logout

def patient_logout_view(request):
    logout(request)
    return redirect('home')   
@login_required
def doctor_dashboard(request):
    try:
        # 1. Fetch the doctor profile
        doctor_profile = Doctor.objects.get(user=request.user)
        
        # 2. Fetch EMERGENCIES (Match the name in your HTML)
        # We fetch pending alerts sent by the receptionist to this doctor
        emergencies = EmergencyAlert.objects.filter(doctor=request.user, status="pending").order_by('-created_at')
        
        # 3. Check if there is an ACTIVE emergency
        active_emergency = emergencies.exists()
        
        # 4. Fetch TODAY'S Appointments
        today = timezone.now().date()
        appointments = Appointment.objects.filter(
            doctor=doctor_profile, 
            appointment_date=today
        ).order_by('queue_number')

        # 5. Get the CURRENT patient (Now Serving)
        current_patient = appointments.filter(status="in_progress").first()

        # 6. Fetch UNREAD Notifications
        notifications = DoctorNotification.objects.filter(doctor=request.user, is_read=False)

    except Doctor.DoesNotExist:
        messages.error(request, "Access Denied: You do not have a Doctor profile.")
        return redirect('patient_dashboard')

    return render(request, 'doctors/doctor_dashboard.html', {
        'doctor': doctor_profile,
        'emergencies': emergencies,        # Corrected name
        'active_emergency': active_emergency,
        'appointments': appointments,
        'current_patient': current_patient,
        'notifications': notifications,
    }) 