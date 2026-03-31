from django.contrib import admin
from .models import Doctor, Appointment, EmergencyAlert, DoctorNotification, ContactMessage, Gallery

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Changed 'experience_years' to 'experience' to match your model
    list_display = ('user', 'specialization', 'experience') 
    search_fields = ('user__last_name', 'specialization')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    # Added disease to the display so you can see your teacher's new feature
    list_display = ('patient_name', 'doctor', 'appointment_date', 'disease', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('patient_name', 'disease')

@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'status', 'created_at')
    list_filter = ('status',)

@admin.register(DoctorNotification)
class DoctorNotificationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'appointment', 'is_read', 'created_at')

admin.site.register(ContactMessage)
admin.site.register(Gallery)