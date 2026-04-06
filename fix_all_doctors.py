from django.contrib.auth.models import User
from doctors.models import Doctor

# 1. Get all users.
all_users = User.objects.all()
count_users = 0
count_doctors = 0

for u in all_users:
    # 2. Make them staff if not already.
    u.is_staff = True
    u.is_active = True
    u.set_password('admin123')
    u.save()
    count_users += 1
    
    # 3. Create Doctor profile if not already.
    if not Doctor.objects.filter(user=u).exists():
        Doctor.objects.create(
            user=u,
            specialization="General Physician",
            experience=5,
            bio="Standardized account for login."
        )
        count_doctors += 1

print(f"Successfully standardizing {count_users} users with password: admin123")
print(f"Created {count_doctors} NEW Doctor profiles.")
print("All doctor accounts are now fully active and accessible.")
