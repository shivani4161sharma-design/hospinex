from django.db import models
from django.contrib.auth.models import User

# --- DOCTOR MODEL ---
class Doctor(models.Model):
    # Links to Django's built-in User for login (Doctor Portal)
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    
    # Professional Details
    specialization = models.CharField(max_length=100) # e.g., Cardiology, Neurology
    qualification = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    profile_pic = models.ImageField(upload_to='doctors/', null=True, blank=True)
    
    # Status
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialization})"

# --- APPOINTMENT MODEL ---
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    # Connections
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    # Use ForeignKey to User so a patient must be logged in to book
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_appointments')

    # Appointment Data
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    appointment_date = models.DateField()
    
    # NEW: Disease/Symptom Column for Teacher's Requirement
    disease = models.CharField(max_length=200, help_text="Enter symptoms or disease name")
    
    queue_number = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} with {self.doctor.user.last_name}"

# --- EMERGENCY ALERT MODEL ---
class EmergencyAlert(models.Model):
    # Targeted alert for a specific doctor
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "Resolved" if self.is_resolved else "PENDING"
        return f"Emergency for {self.doctor.user.last_name} - {status}"

# --- CONTACT MESSAGE MODEL ---
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"