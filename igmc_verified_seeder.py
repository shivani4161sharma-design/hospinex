"""
IGMC Shimla Verified Doctor Seeder
===================================
Seeds doctors from IGMC Shimla who have verified photos on the official website.
Photos are either already downloaded in media/doctors/ or will be downloaded now.

Departments covered (matching our website):
  - Anesthesia         -> Anaesthesia dept on IGMC
  - Emergency          -> Emergency Medicine on IGMC
  - Ophthalmology      -> Ophthalmology (Eye) on IGMC
  - Orthopedics        -> Orthopaedics on IGMC
  - Pediatrics         -> Paediatrics on IGMC
  - Radiotherapy       -> Radiotherapy on IGMC
  - General Surgery    -> Surgery on IGMC
  - Dermatology        -> Dermatology on IGMC

Run: python igmc_verified_seeder.py
"""

import os
import sys
import django
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from django.core.files import File
from doctors.models import Doctor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_DOCTORS = os.path.join(BASE_DIR, 'media', 'doctors')

# =====================================================================
# VERIFIED IGMC SHIMLA DOCTORS (with photos found on official website)
# photo_file = filename in media/doctors/ that was previously downloaded
# photo_url  = fallback URL if file not already present
# =====================================================================
IGMC_DOCTORS = [

    # ── ANESTHESIA ────────────────────────────────────────────────────
    {
        "first_name": "Ajay",
        "last_name": "Sood",
        "specialization": "Anesthesia",
        "designation": "Professor & Head",
        "qualification": "MD - Anaesthesia",
        "experience": 22,
        "bio": "Prof. Ajay Sood is the Head of Department of Anaesthesia at IGMC Shimla with over 22 years of expertise in general anesthesia, regional anesthesia, and critical care medicine.",
        "photo_file": "Ajay20Sood.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Ajay%20Sood.jpg",
    },
    {
        "first_name": "Dara Singh",
        "last_name": "Negi",
        "specialization": "Anesthesia",
        "designation": "Professor",
        "qualification": "MD - Anaesthesia",
        "experience": 18,
        "bio": "Dr. Dara Singh Negi is a senior Professor of Anaesthesia at IGMC Shimla specializing in paediatric anaesthesia and pain management.",
        "photo_file": "ddaranegi.png",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/ddaranegi.png",
    },
    {
        "first_name": "Ravi Kant",
        "last_name": "Dogra",
        "specialization": "Anesthesia",
        "designation": "Professor",
        "qualification": "MD - Anaesthesia",
        "experience": 15,
        "bio": "Dr. Ravi Kant Dogra is a Professor of Anaesthesia at IGMC Shimla with expertise in obstetric anaesthesia and critical care.",
        "photo_file": "Ravi20kant20Dogra.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Ravi%20kant%20Dogra.jpg",
    },

    # ── EMERGENCY MEDICINE ────────────────────────────────────────────
    {
        "first_name": "Rajiv",
        "last_name": "Kundlas",
        "specialization": "Emergency",
        "designation": "Assistant Professor",
        "qualification": "MBBS, MD - Emergency Medicine",
        "experience": 10,
        "bio": "Dr. Rajiv Kundlas is an Emergency Medicine specialist at IGMC Shimla, managing trauma cases and acute care with precision and speed.",
        "photo_file": "Rajiv20Kundlass20Vlog.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Rajiv%20Kundlas's%20Vlog.jpg",
    },

    # ── OPHTHALMOLOGY ─────────────────────────────────────────────────
    {
        "first_name": "Ram Lal",
        "last_name": "Sharma",
        "specialization": "Ophthalmology",
        "designation": "Professor & Head",
        "qualification": "MS - Ophthalmology",
        "experience": 24,
        "bio": "Prof. Ram Lal Sharma heads the Department of Ophthalmology at IGMC Shimla. He is an authority in cataract surgery, vitreo-retinal surgery, and complex corneal procedures.",
        "photo_file": "RAM20SHARMA.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/RAM%20SHARMA.jpeg",
    },
    {
        "first_name": "Vinod",
        "last_name": "Kashyap",
        "specialization": "Ophthalmology",
        "designation": "Professor",
        "qualification": "MS - Ophthalmology",
        "experience": 19,
        "bio": "Dr. Vinod Kashyap is a Professor of Ophthalmology at IGMC Shimla with extensive experience in glaucoma management and phacoemulsification.",
        "photo_file": "vinod20kashyap.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/vinod%20kashyap.jpeg",
    },
    {
        "first_name": "Praveen",
        "last_name": "Panwar",
        "specialization": "Ophthalmology",
        "designation": "Professor",
        "qualification": "MS - Ophthalmology",
        "experience": 16,
        "bio": "Dr. Praveen Panwar specializes in pediatric ophthalmology and squint surgery at IGMC Shimla.",
        "photo_file": "praveen20panwar.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/praveen%20panwar.jpeg",
    },

    # ── ORTHOPEDICS ──────────────────────────────────────────────────
    {
        "first_name": "Vineet",
        "last_name": "Aggarwal",
        "specialization": "Orthopedics",
        "designation": "Professor & Head",
        "qualification": "MS - Orthopaedics",
        "experience": 23,
        "bio": "Prof. Vineet Aggarwal is the Head of Orthopaedics at IGMC Shimla, known for his excellence in joint replacement surgery and complex trauma management.",
        "photo_file": "vineet_aggarwal_orthopedics.bmp",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/v2.bmp",
    },
    {
        "first_name": "Desh Raj",
        "last_name": "Chandel",
        "specialization": "Orthopedics",
        "designation": "Professor",
        "qualification": "MS - Orthopaedics",
        "experience": 20,
        "bio": "Dr. Desh Raj Chandel is a Professor of Orthopaedics at IGMC Shimla specializing in spinal surgery and sports injuries.",
        "photo_file": "Desh20Raj20Chandel.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Desh%20Raj%20Chandel.jpg",
    },
    {
        "first_name": "Rajesh",
        "last_name": "Sood",
        "specialization": "Orthopedics",
        "designation": "Professor",
        "qualification": "MS - Orthopaedics",
        "experience": 17,
        "bio": "Dr. Rajesh Sood at IGMC Shimla specializes in paediatric orthopaedics and limb reconstruction surgeries.",
        "photo_file": "rajeshsood.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/rajeshsood.jpeg",
    },

    # ── PEDIATRICS ────────────────────────────────────────────────────
    {
        "first_name": "Bhagat",
        "last_name": "Thakur",
        "specialization": "Pediatrics",
        "designation": "Professor",
        "qualification": "MD - Paediatrics",
        "experience": 18,
        "bio": "Dr. Bhagat Thakur is a senior Paediatrics Professor at IGMC Shimla with expertise in neonatology and paediatric infectious diseases.",
        "photo_file": "Bhagat20Thakur.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Bhagat%20Thakur.jpg",
    },
    {
        "first_name": "Pratima",
        "last_name": "Thakur",
        "specialization": "Pediatrics",
        "designation": "Associate Professor",
        "qualification": "MD - Paediatrics",
        "experience": 14,
        "bio": "Dr. Pratima Thakur is an Associate Professor in Paediatrics at IGMC Shimla focusing on childhood nutrition and developmental disorders.",
        "photo_file": "Pratima20Thakur.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Pratima%20Thakur.jpeg",
    },
    {
        "first_name": "Parveen",
        "last_name": "Bhardwaj",
        "specialization": "Pediatrics",
        "designation": "Associate Professor",
        "qualification": "MD - Paediatrics",
        "experience": 12,
        "bio": "Dr. Parveen Bhardwaj is an Associate Professor of Paediatrics at IGMC Shimla with expertise in paediatric emergencies and NICU management.",
        "photo_file": "Parveen20Bhardwaj.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Parveen%20Bhardwaj.jpg",
    },

    # ── RADIOTHERAPY ──────────────────────────────────────────────────
    {
        "first_name": "Manish",
        "last_name": "Gupta",
        "specialization": "Radiotherapy",
        "designation": "Professor & Head",
        "qualification": "MD - Radiation Oncology",
        "experience": 20,
        "bio": "Prof. Manish Gupta is the Head of Radiotherapy at IGMC Shimla, specializing in radiation oncology and targeted cancer therapies.",
        "photo_file": "Manish20Gupta.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Manish%20Gupta.jpeg",
    },
    {
        "first_name": "Shailee",
        "last_name": "Fotedar",
        "specialization": "Radiotherapy",
        "designation": "Associate Professor",
        "qualification": "MD - Radiotherapy",
        "experience": 14,
        "bio": "Dr. Shailee Fotedar is an Associate Professor of Radiotherapy at IGMC Shimla with expertise in brachytherapy and palliative oncology.",
        "photo_file": "Shailee20Fotedar.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Shailee%20Fotedar.jpg",
    },
    {
        "first_name": "Deepak",
        "last_name": "Tuli",
        "specialization": "Radiotherapy",
        "designation": "Assistant Professor",
        "qualification": "MD - Radiation Oncology",
        "experience": 10,
        "bio": "Dr. Deepak Tuli is an Assistant Professor in the Department of Radiotherapy at IGMC Shimla specializing in conformal radiation therapy.",
        "photo_file": "Deepak20Tuli.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Deepak%20Tuli.jpg",
    },

    # ── GENERAL SURGERY ──────────────────────────────────────────────
    {
        "first_name": "Ved Kumar",
        "last_name": "Sharma",
        "specialization": "General Surgery",
        "designation": "Professor & Head",
        "qualification": "MS - General Surgery",
        "experience": 25,
        "bio": "Prof. Ved Kumar Sharma is the Head of General Surgery at IGMC Shimla. He is a highly experienced surgeon in hepato-biliary, laparoscopic, and oncological surgeries.",
        "photo_file": "Ved20Kumar20Sharma.jpeg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Ved%20Kumar%20Sharma.jpeg",
    },
    {
        "first_name": "Arun",
        "last_name": "Chauhan",
        "specialization": "General Surgery",
        "designation": "Professor",
        "qualification": "MS - General Surgery",
        "experience": 18,
        "bio": "Dr. Arun Chauhan is a Professor of Surgery at IGMC Shimla with expertise in laparoscopic cholecystectomy and colorectal surgery.",
        "photo_file": "Arun20Chauhan.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Arun%20Chauhan.jpg",
    },
    {
        "first_name": "Balwant",
        "last_name": "Singh",
        "specialization": "General Surgery",
        "designation": "Associate Professor",
        "qualification": "MS - General Surgery",
        "experience": 14,
        "bio": "Dr. Balwant Singh is an Associate Professor of General Surgery at IGMC Shimla skilled in endoscopic and minimally invasive procedures.",
        "photo_file": "Balwant.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Balwant.jpg",
    },

    # ── DERMATOLOGY ──────────────────────────────────────────────────
    {
        "first_name": "Ghanshyam",
        "last_name": "Verma",
        "specialization": "Dermatology",
        "designation": "Professor & Head",
        "qualification": "MD - Dermatology, Venereology & Leprosy",
        "experience": 22,
        "bio": "Prof. Ghanshyam Verma is the Head of the Department of Dermatology at IGMC Shimla. He has pioneered dermatological research in Himachal Pradesh.",
        "photo_file": "DrGhanshyamVerma.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/DrGhanshyamVerma.jpg",
    },
    {
        "first_name": "Reena",
        "last_name": "Sharma",
        "specialization": "Dermatology",
        "designation": "Associate Professor",
        "qualification": "MD - Dermatology",
        "experience": 15,
        "bio": "Dr. Reena Sharma is an Associate Professor of Dermatology at IGMC Shimla with expertise in cosmetic dermatology and skin allergy management.",
        "photo_file": "Reema.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/Reema.jpg",
    },
    {
        "first_name": "Ajeet",
        "last_name": "Negi",
        "specialization": "Dermatology",
        "designation": "Assistant Professor",
        "qualification": "MD - Dermatology",
        "experience": 10,
        "bio": "Dr. Ajeet Negi is an Assistant Professor of Dermatology at IGMC Shimla specializing in trichology and contact dermatitis.",
        "photo_file": "AJEET_NEGI.jpg",
        "photo_url":  "http://igmcshimla.edu.in/ig/images/avatars/AJEET_NEGI.jpg",
    },
]


def seed_doctors():
    print("\n" + "="*60)
    print("  IGMC Shimla Verified Doctor Seeder")
    print("="*60)

    created_count = 0
    updated_count = 0
    photo_success = 0
    photo_fail = 0

    for data in IGMC_DOCTORS:
        first = data['first_name']
        last  = data['last_name']
        spec  = data['specialization']

        # Build a clean username
        username = f"{first.lower().replace(' ', '').replace('.', '')}.{last.lower().replace(' ', '').replace('.', '')}"

        print(f"\n→ Processing: Dr. {first} {last} ({spec})")

        # Create or get the User
        user, u_created = User.objects.get_or_create(username=username)
        if u_created:
            user.set_password('hospital123')
            user.first_name = first
            user.last_name  = last
            user.is_staff   = True
            user.email      = f"{username}@igmcshimla.edu.in"
            user.save()
            print(f"   ✔ User created: {username}")
            created_count += 1
        else:
            # Make sure the user is staff (in case they existed before)
            if not user.is_staff:
                user.is_staff = True
                user.save()
            print(f"   ↺ User already exists: {username}")
            updated_count += 1

        # Create or get the Doctor profile
        doctor, d_created = Doctor.objects.get_or_create(user=user)
        doctor.specialization = spec
        doctor.experience     = data.get('experience', 12)
        doctor.bio            = data.get('bio', f"Experienced {spec} specialist at IGMC Shimla.")

        # ── Attach photo ──────────────────────────────────────────
        photo_filename = data.get('photo_file', '')
        local_photo    = os.path.join(MEDIA_DOCTORS, photo_filename)

        if photo_filename and os.path.isfile(local_photo) and os.path.getsize(local_photo) > 500:
            # File exists and seems valid — attach it from disk
            if not doctor.photo or not os.path.isfile(doctor.photo.path):
                try:
                    with open(local_photo, 'rb') as f:
                        doctor.photo.save(photo_filename, File(f), save=False)
                    print(f"   📷 Photo attached from disk: {photo_filename}")
                    photo_success += 1
                except Exception as e:
                    print(f"   ⚠ Could not attach photo: {e}")
                    photo_fail += 1
            else:
                print(f"   📷 Photo already set: {doctor.photo.name}")
                photo_success += 1
        else:
            # Try downloading from IGMC website
            photo_url = data.get('photo_url', '')
            if photo_url:
                try:
                    import requests
                    from django.core.files.temp import NamedTemporaryFile
                    print(f"   ⬇  Downloading from IGMC: {photo_url}")
                    resp = requests.get(photo_url, timeout=15, verify=False)
                    if resp.status_code == 200 and len(resp.content) > 500:
                        img_temp = NamedTemporaryFile(delete=True, suffix=os.path.splitext(photo_filename)[1] or '.jpg')
                        img_temp.write(resp.content)
                        img_temp.flush()
                        save_name = photo_filename or photo_url.split('/')[-1]
                        doctor.photo.save(save_name, File(img_temp), save=False)
                        print(f"   ✔ Photo downloaded & saved: {save_name}")
                        photo_success += 1
                    else:
                        print(f"   ✗ Download failed (status {resp.status_code})")
                        photo_fail += 1
                except Exception as e:
                    print(f"   ✗ Download error: {e}")
                    photo_fail += 1
            else:
                print(f"   ✗ No photo source available")
                photo_fail += 1

        doctor.save()
        print(f"   ✔ Doctor profile saved.")

    print("\n" + "="*60)
    print(f"  DONE!")
    print(f"  Doctors created : {created_count}")
    print(f"  Doctors updated : {updated_count}")
    print(f"  Photos attached : {photo_success}")
    print(f"  Photos failed   : {photo_fail}")
    print("="*60 + "\n")


if __name__ == '__main__':
    seed_doctors()
