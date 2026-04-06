from django.contrib.auth.models import User
from doctors.models import Doctor

doctors = Doctor.objects.all()
count = 0
for d in doctors:
    u = d.user
    u.is_staff = True
    u.is_active = True
    u.set_password('admin123')
    u.save()
    count += 1
print(f"Successfully configured {count} doctor accounts for portal access.")
print("All doctor passwords are now set to: admin123")
