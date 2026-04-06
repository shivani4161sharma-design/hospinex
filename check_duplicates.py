from django.contrib.auth.models import User
from doctors.models import Doctor, Appointment, EmergencyAlert

duplicates = ["Ajay Sood", "Desh Raj Chandel", "Amit Sharma", "Neeti Sharma", "Ram Singh", "Reena Sharma"]

for name in duplicates:
    print(f"\n--- Analyzing Duplicate: {name} ---")
    users = User.objects.filter(first_name=' '.join(name.split()[:-1]), last_name=name.split()[-1])
    if not users.exists(): # Try full name check
        users = [u for u in User.objects.all() if u.get_full_name() == name]
    
    for u in users:
        doctor_profile = Doctor.objects.filter(user=u).first()
        appts = Appointment.objects.filter(doctor=doctor_profile).count() if doctor_profile else 0
        alerts = EmergencyAlert.objects.filter(doctor=u).count()
        print(f"User: {u.username} (ID: {u.id}) | Staff: {u.is_staff} | Apps: {appts} | Alerts: {alerts}")
