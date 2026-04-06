from django.contrib.auth.models import User
from doctors.models import Doctor, Appointment, EmergencyAlert, DoctorNotification
from django.db.models import Count

def merge_doctors():
    # Identify duplicate names
    all_users = User.objects.all()
    names = [(u.get_full_name(), u) for u in all_users]
    
    unique_names = set(n[0] for n in names)
    
    for name in unique_names:
        if not name.strip(): continue
        
        duplicates = [u for n, u in names if n == name]
        if len(duplicates) > 1:
            print(f"Merging duplicates for: {name}")
            # Keep the one with a standard username (like dot or underscore) or the first one
            # Actually, keep the one that most likely corresponds to the current session (ajay.sood)
            # Or just pick the first one and move everything.
            
            # Identify the best one to keep (prefer the one with existing appointments)
            keep_user = duplicates[0]
            max_data = -1
            
            for u in duplicates:
                data_count = Appointment.objects.filter(doctor__user=u).count() + EmergencyAlert.objects.filter(doctor=u).count()
                if data_count > max_data:
                    max_data = data_count
                    keep_user = u
            
            others = [u for u in duplicates if u != keep_user]
            
            # Ensure the kept user has a Doctor profile
            keep_doctor, _ = Doctor.objects.get_or_create(user=keep_user, defaults={'specialization': 'General'})
            
            for other_user in others:
                other_doctor = Doctor.objects.filter(user=other_user).first()
                
                # Move Appointments
                if other_doctor:
                    Appointment.objects.filter(doctor=other_doctor).update(doctor=keep_doctor)
                
                # Move Emergencies
                EmergencyAlert.objects.filter(doctor=other_user).update(doctor=keep_user)
                
                # Move Notifications
                DoctorNotification.objects.filter(doctor=other_user).update(doctor=keep_user)
                
                # Delete Other Doctor Profile
                if other_doctor:
                    other_doctor.delete()
                
                # Delete other User
                print(f"  Deleting duplicate user: {other_user.username} (ID: {other_user.id})")
                other_user.delete()
                
    print("Merge Complete!")

merge_doctors()
