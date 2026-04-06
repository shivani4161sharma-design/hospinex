from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# --- DOCTOR MODEL ---
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    specialization = models.CharField(blank=True, max_length=100)
    experience = models.PositiveIntegerField(blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.last_name}"

# --- APPOINTMENT MODEL ---
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    TIME_SLOTS = [
        ('09:00 AM', '09:00 AM'), ('10:00 AM', '10:00 AM'), 
        ('11:00 AM', '11:00 AM'), ('12:00 PM', '12:00 PM'), 
        ('02:00 PM', '02:00 PM'), ('03:00 PM', '03:00 PM'), 
        ('04:00 PM', '04:00 PM')
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField(max_length=254)
    patient_phone = models.CharField(max_length=15)
    appointment_date = models.DateField()
    time_slot = models.CharField(max_length=20, choices=TIME_SLOTS, default='09:00 AM')
    
    # TEACHER'S NEW REQUIREMENT: Disease field
    disease = models.CharField(max_length=200, default="Not Specified")
    
    queue_number = models.PositiveIntegerField(blank=True, null=True)
    is_emergency = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS_CHOICES, default='waiting', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['appointment_date', 'queue_number']

    def __str__(self):
        return f"{self.patient_name} - {self.appointment_date}"

# --- EMERGENCY ALERT MODEL ---
class EmergencyAlert(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('seen', 'Seen'),
        ('resolved', 'Resolved')
    ]
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    patient_name = models.CharField(max_length=100)
    patient_phone = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default='pending', max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

# --- DOCTOR NOTIFICATION MODEL ---
class DoctorNotification(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

# --- CONTACT MESSAGE MODEL ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
# --- CHAT MESSAGE MODEL ---
class ChatMessage(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    message = models.TextField()
    sender = models.CharField(max_length=20) # 'doctor' or 'patient'
    created_at = models.DateTimeField(auto_now_add=True)

# --- GALLERY MODEL ---
class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(blank=True, max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)