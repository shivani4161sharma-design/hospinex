from django.contrib.auth.models import User
from doctors.models import Doctor

staff_users = User.objects.filter(is_staff=True)
created_count = 0

for u in staff_users:
    if not Doctor.objects.filter(user=u).exists():
        Doctor.objects.create(
            user=u,
            specialization="General Physician",
            experience=5,
            bio="Default profile automatically created."
        )
        created_count += 1

print(f"Success! Created {created_count} missing Doctor profiles.")
print("Now all Admin staff members can log in to the Doctor Portal.")
