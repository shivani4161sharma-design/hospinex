from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, Appointment, EmergencyAlert, DoctorNotification, ContactMessage, Gallery


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_photo_thumb', 'full_name', 'specialization', 'designation_badge', 'experience_years', 'view_profile_link')
    list_display_links = ('doctor_photo_thumb', 'full_name')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('specialization',)
    list_per_page = 20
    ordering = ('specialization', 'user__last_name')

    fieldsets = (
        ('👤 Personal Information', {
            'fields': ('user', 'photo'),
            'classes': ('wide',),
        }),
        ('🏥 Professional Details', {
            'fields': ('specialization', 'experience', 'bio'),
            'classes': ('wide',),
        }),
    )

    def doctor_photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:52px;height:52px;object-fit:cover;border-radius:50%;'
                'border:3px solid #27ae60;box-shadow:0 2px 8px rgba(0,0,0,0.2);" />',
                obj.photo.url
            )
        return format_html(
            '<div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#27ae60,#1e8449);'
            'display:flex;align-items:center;justify-content:center;color:white;font-size:18px;'
            'box-shadow:0 2px 8px rgba(0,0,0,0.2);">{}</div>',
            '👨‍⚕️'
        )
    doctor_photo_thumb.short_description = 'Photo'

    def full_name(self, obj):
        return format_html(
            '<strong style="color:#1a2332;font-size:14px;">Dr. {} {}</strong>',
            obj.user.first_name, obj.user.last_name
        )
    full_name.short_description = 'Doctor Name'
    full_name.admin_order_field = 'user__last_name'

    def designation_badge(self, obj):
        spec = obj.specialization or 'General'
        colors = {
            'Anesthesia':      '#8e44ad',
            'Emergency':       '#e74c3c',
            'Ophthalmology':   '#2980b9',
            'Orthopedics':     '#16a085',
            'Pediatrics':      '#f39c12',
            'Radiotherapy':    '#d35400',
            'General Surgery': '#27ae60',
            'Dermatology':     '#c0392b',
        }
        color = colors.get(spec, '#7f8c8d')
        return format_html(
            '<span style="background:{};color:white;padding:4px 12px;border-radius:20px;'
            'font-size:11px;font-weight:700;letter-spacing:0.5px;">{}</span>',
            color, spec
        )
    designation_badge.short_description = 'Department'

    def experience_years(self, obj):
        if obj.experience:
            return format_html(
                '<span style="color:#27ae60;font-weight:700;">{}</span> yrs',
                obj.experience
            )
        return '—'
    experience_years.short_description = 'Experience'

    def view_profile_link(self, obj):
        return format_html(
            '<a href="/doctors/{}/" target="_blank" style="color:#27ae60;font-weight:600;'
            'text-decoration:none;padding:4px 10px;border:1px solid #27ae60;border-radius:6px;'
            'font-size:11px;">View →</a>',
            obj.id
        )
    view_profile_link.short_description = 'Profile'


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name_styled', 'doctor_name', 'department_badge', 'appointment_date', 'status_badge', 'queue_badge')
    list_filter = ('status', 'appointment_date', 'doctor__specialization')
    search_fields = ('patient_name', 'disease', 'patient_email', 'patient_phone')
    date_hierarchy = 'appointment_date'
    list_per_page = 25
    ordering = ('-appointment_date', 'queue_number')

    fieldsets = (
        ('🧑 Patient Details', {
            'fields': ('patient_name', 'patient_email', 'patient_phone', 'disease'),
            'classes': ('wide',),
        }),
        ('📅 Appointment Details', {
            'fields': ('doctor', 'appointment_date', 'time_slot', 'queue_number', 'is_emergency', 'status'),
            'classes': ('wide',),
        }),
    )

    def patient_name_styled(self, obj):
        icon = '🚨' if obj.is_emergency else '🧑'
        color = '#e74c3c' if obj.is_emergency else '#1a2332'
        return format_html('<strong style="color:{};">{} {}</strong>', color, icon, obj.patient_name)
    patient_name_styled.short_description = 'Patient'

    def doctor_name(self, obj):
        return format_html('Dr. {} {}', obj.doctor.user.first_name, obj.doctor.user.last_name)
    doctor_name.short_description = 'Doctor'

    def department_badge(self, obj):
        return format_html(
            '<span style="font-size:12px;color:#64748b;">{}</span>',
            obj.doctor.specialization
        )
    department_badge.short_description = 'Department'

    def status_badge(self, obj):
        colors = {
            'waiting':     ('#f39c12', '⏳'),
            'in_progress': ('#3498db', '▶️'),
            'completed':   ('#27ae60', '✅'),
            'cancelled':   ('#e74c3c', '❌'),
        }
        color, icon = colors.get(obj.status, ('#7f8c8d', '•'))
        label = obj.get_status_display()
        return format_html(
            '<span style="color:{};font-weight:700;font-size:12px;">{} {}</span>',
            color, icon, label
        )
    status_badge.short_description = 'Status'

    def queue_badge(self, obj):
        if obj.queue_number:
            return format_html(
                '<span style="background:#f0fdf4;color:#27ae60;font-weight:800;'
                'padding:3px 10px;border-radius:20px;font-size:13px;">#{}</span>',
                obj.queue_number
            )
        return '—'
    queue_badge.short_description = 'Queue #'


@admin.register(EmergencyAlert)
class EmergencyAlertAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'status_badge', 'created_at')
    list_filter = ('status',)
    ordering = ('-created_at',)

    def status_badge(self, obj):
        colors = {'pending': '#e74c3c', 'seen': '#f39c12', 'resolved': '#27ae60'}
        color = colors.get(obj.status, '#7f8c8d')
        return format_html(
            '<span style="color:{};font-weight:700;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(DoctorNotification)
class DoctorNotificationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'appointment', 'read_status', 'created_at')
    list_filter = ('is_read',)

    def read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="color:#27ae60;font-weight:700;">{}</span>', '✅ Read')
        return format_html('<span style="color:#e74c3c;font-weight:700;">{}</span>', '🔔 Unread')
    read_status.short_description = 'Read Status'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message', 'created_at')
    search_fields = ('name', 'email')
    ordering = ('-created_at',)

    def short_message(self, obj):
        return obj.message[:60] + '...' if len(obj.message) > 60 else obj.message
    short_message.short_description = 'Message Preview'


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('gallery_thumb', 'title', 'uploaded_at')

    def gallery_thumb(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:45px;object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return '—'
    gallery_thumb.short_description = 'Preview'