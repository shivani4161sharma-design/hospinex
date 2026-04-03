import os
import sys
import django
import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
sys.path.append(os.getcwd())
django.setup()

from doctors.models import Doctor

DOCTORS_DATA = [
    # Pediatrics
    {"first_name": "Parveen", "last_name": "Bhardwaj", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Parveen%20Bhardwaj.jpg"},
    {"first_name": "Mangla", "last_name": "Sood", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Mangla%20Sood.jpg"},
    {"first_name": "Bhagat", "last_name": "Thakur", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Bhagat%20Thakur.jpg"},
    {"first_name": "Pratima", "last_name": "Thakur", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Pratima%20Thakur.jpeg"},
    {"first_name": "Jiya", "last_name": "Doctor", "specialization": "Pediatrics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/jiya.jpeg"},

    # Radiotherapy
    {"first_name": "Manish", "last_name": "Gupta", "specialization": "Radiotherapy", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Manish%20Gupta.jpeg"},
    {"first_name": "Shailee", "last_name": "Fotedar", "specialization": "Radiotherapy", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Shailee%20Fotedar.jpg"},
    {"first_name": "Purnima", "last_name": "Thakur", "specialization": "Radiotherapy", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/purnima%20thakur.jpeg"},
    {"first_name": "Deepak", "last_name": "Tuli", "specialization": "Radiotherapy", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Deepak%20Tuli.jpg"},

    # Emergency Medicine
    {"first_name": "Rajiv", "last_name": "Kundlas", "specialization": "Emergency Medicine", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Rajiv%20Kundlas's%20Vlog.jpg"},

    # Ophthalmology
    {"first_name": "Ram Lal", "last_name": "Sharma", "specialization": "Ophthalmology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/RAM%20SHARMA.jpeg"},
    {"first_name": "Vinod", "last_name": "Kashyap", "specialization": "Ophthalmology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/vinod%20kashyap.jpeg"},
    {"first_name": "Praveen", "last_name": "Panwar", "specialization": "Ophthalmology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/praveen%20panwar.jpeg"},
    {"first_name": "Kalpana", "last_name": "Sharma", "specialization": "Ophthalmology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/kalpana%20sharma.jpeg"},

    # General Surgery
    {"first_name": "D.S.", "last_name": "Sharma", "specialization": "General Surgery", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/dks.jpg"},
    {"first_name": "Ved Kumar", "last_name": "Sharma", "specialization": "General Surgery", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Ved%20Kumar%20Sharma.jpeg"},
    {"first_name": "Arun", "last_name": "Chauhan", "specialization": "General Surgery", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Arun%20Chauhan.jpg"},
    {"first_name": "Balwant", "last_name": "Doctor", "specialization": "General Surgery", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Balwant.jpg"},

    # Orthopedics
    {"first_name": "Vineet", "last_name": "Aggarwal", "specialization": "Orthopedics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/v2.bmp"},
    {"first_name": "B.D.S.", "last_name": "Chandel", "specialization": "Orthopedics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Desh%20Raj%20Chandel.jpg"},
    {"first_name": "Rajesh", "last_name": "Sood", "specialization": "Orthopedics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/rajeshsood.jpeg"},
    {"first_name": "S.", "last_name": "Sud", "specialization": "Orthopedics", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/SSud.jpg"},

    # Anesthesia
    {"first_name": "Ajay", "last_name": "Sood", "specialization": "Anesthesia", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Ajay%20Sood.jpg"},
    {"first_name": "Dara Singh", "last_name": "Negi", "specialization": "Anesthesia", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/ddaranegi.png"},
    {"first_name": "Aparna", "last_name": "Sharma", "specialization": "Anesthesia", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Aparna%20harma.jpg"},
    {"first_name": "Ravi Kant", "last_name": "Dogra", "specialization": "Anesthesia", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Ravi%20kant%20Dogra.jpg"},
    {"first_name": "Kartik", "last_name": "Syal", "specialization": "Anesthesia", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Kartik_Syal.jpeg"},

    # Dermatology
    {"first_name": "G.K.", "last_name": "Verma", "specialization": "Dermatology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/DrGhanshyamVerma.jpg"},
    {"first_name": "Reema", "last_name": "Doctor", "specialization": "Dermatology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/Reema.jpg"},
    {"first_name": "Ajeet", "last_name": "Negi", "specialization": "Dermatology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/AJEET_NEGI.jpg"},
    {"first_name": "Sandhya", "last_name": "Chauhan", "specialization": "Dermatology", "photo_url": "http://www.igmcshimla.edu.in/ig/images/avatars/SandhyaChauhan.jpg"},
]

def seed_doctors():
    for data in DOCTORS_DATA:
        username = f"{data['first_name'].lower().replace(' ', '')}.{data['last_name'].lower().replace(' ', '')}"
        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password('hospital123')
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.is_staff = True
            user.save()
        
        doctor, d_created = Doctor.objects.get_or_create(user=user)
        doctor.specialization = data['specialization']
        doctor.experience = 10 # Default
        doctor.bio = f"Experienced specialist in {data['specialization']} at IGMC Shimla."
        
        # Download and set photo
        try:
            print(f"Downloading photo for {data['first_name']} {data['last_name']}...")
            response = requests.get(data['photo_url'], timeout=10)
            if response.status_code == 200:
                img_temp = NamedTemporaryFile(delete=True)
                img_temp.write(response.content)
                img_temp.flush()
                
                filename = data['photo_url'].split('/')[-1]
                doctor.photo.save(filename, File(img_temp), save=True)
                print(f"Successfully saved photo for {data['first_name']}.")
            else:
                print(f"Failed to download photo for {data['first_name']}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error downloading photo for {data['first_name']}: {e}")
        
        doctor.save()

if __name__ == "__main__":
    seed_doctors()
    print("Seeding completed.")
