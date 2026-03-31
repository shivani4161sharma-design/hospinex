from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'patient_name',
            'patient_email',
            'patient_phone',
            'doctor',
            'appointment_date',
            'message',
        ]

        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }
