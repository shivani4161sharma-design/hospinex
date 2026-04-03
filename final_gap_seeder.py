import os
import sys
import requests
import django
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
sys.path.append(os.getcwd())
django.setup()

from doctors.models import Doctor

GAPS_DATA = [
    # Emergency Medicine
    {"first_name": "Vivek", "last_name": "Chauhan", "specialization": "Emergency Medicine", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/VivekChauhan.jpg"},
    
    # Radiotherapy
    {"first_name": "Vikas", "last_name": "Fotedar", "specialization": "Radiotherapy", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Shailee%20Fotedar.jpg"},
    {"first_name": "Manish", "last_name": "Gupta", "specialization": "Radiotherapy", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Manish%20Gupta.jpeg"},
    
    # Pediatrics
    {"first_name": "Parveen", "last_name": "Bhardwaj", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Parveen%20Bhardwaj.jpg"},
    {"first_name": "Mangla", "last_name": "Sood", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Mangla%20Sood.jpg"},
    
    # General Surgery
    {"first_name": "Dhiraj", "last_name": "Sharma", "specialization": "General Surgery", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/dks.jpg"},
    {"first_name": "Balwant", "last_name": "Doctor", "specialization": "General Surgery", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Balwant.jpg"},

    # Orthopedics
    {"first_name": "Vineet", "last_name": "Aggarwal", "specialization": "Orthopedics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/v2.bmp"},
    {"first_name": "Desh Raj", "last_name": "Chandel", "specialization": "Orthopedics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Desh%20Raj%20Chandel.jpg"},
]

def seed_gaps():
    for data in GAPS_DATA:
        username = f"gap.{data['first_name'].lower().replace(' ', '')}.{data['last_name'].lower().replace(' ', '')}"
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('hospital123')
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = True
            user.save()
        
        doctor, d_created = Doctor.objects.get_or_create(user=user)
        doctor.specialization = data['specialization']
        doctor.experience = 15
        doctor.bio = f"Experienced medical professional in {data['specialization']} at IGMC Shimla."
        
        try:
            print(f"Downloading gap photo for {data['first_name']} {data['last_name']}...")
            url = data['photo_url'].replace(' ', '%20')
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=False, suffix=".jpg")
                img_temp.write(response.content)
                img_temp.close()
                
                with open(img_temp.name, "rb") as f:
                    filename = data['photo_url'].split('/')[-1].replace(' ', '_')
                    if not filename: filename = "doctor.jpg"
                    doctor.photo.save(filename, File(f), save=True)
                
                os.remove(img_temp.name)
                print(f"  ✔ Saved.")
            else:
                print(f"  ✘ Failed: {response.status_code}")
        except Exception as e:
            print(f"  ✘ Error: {e}")
        
        doctor.save()

if __name__ == "__main__":
    seed_gaps()
    print("Gap seeding completed.")
