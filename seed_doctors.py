"""
Full IGMC doctor seeder:
- Downloads real photos from igmcshimla.edu.in
- Creates User + Doctor records for all 8 departments
- 3-4 doctors per department (real names from faculty pages)
"""
import os, sys, django, urllib.request, shutil, re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from django.contrib.auth.models import User
from doctors.models import Doctor

BASE_URL  = "http://www.igmcshimla.edu.in/ig/images/avatars/"
MEDIA_DIR = Path(__file__).resolve().parent / "media" / "doctors"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# ────────────────────────────────────────────────────────────
# REAL doctors scraped from igmcshimla.edu.in faculty pages
# Format: (first, last, specialization, experience, bio, photo_filename)
# ────────────────────────────────────────────────────────────
DOCTORS = [

    # ANESTHESIA ─────────────────────────────────────────────
    ("Ajay",    "Sood",      "Anesthesia", 28,
     "Professor & Head of Anesthesia. Expert in regional anesthesia, critical care, and pain management with over two decades of surgical support experience.",
     "Ajay Sood.jpg"),

    ("Dara",    "Singh",     "Anesthesia", 22,
     "Senior Professor specializing in cardiac anesthesia and intensive care unit management.",
     "drsodhi.jpeg"),

    ("Manoj",   "Kumar",     "Anesthesia", 18,
     "Professor with expertise in neuro-anesthesia and obstetric anesthesia.",
     "dmkpi.png"),

    ("Aparna",  "Sharma",    "Anesthesia", 14,
     "Associate Professor specializing in pediatric anesthesia and airway management.",
     "Aparna harma.jpg"),

    # GENERAL SURGERY ─────────────────────────────────────────
    ("Puneet",  "Mahajan",   "General Surgery", 26,
     "Professor & Head of General Surgery. Specializes in laparoscopic and oncological surgeries with extensive experience in complex abdominal procedures.",
     "UK.jpeg"),

    ("Dhruv",   "Sharma",    "General Surgery", 20,
     "Professor with expertise in endoscopic and thoracic surgery.",
     "dks.jpg"),

    ("Ved Kumar","Sharma",   "General Surgery", 17,
     "Associate Professor specializing in hepatobiliary and trauma surgery.",
     "Ved Kumar Sharma.jpeg"),

    ("Ashok",   "Kaundal",   "General Surgery", 15,
     "Associate Professor with expertise in colorectal surgery and endoscopy.",
     "ashok kaundal.jpeg"),

    # DERMATOLOGY ─────────────────────────────────────────────
    ("G.K.",    "Verma",     "Dermatology", 30,
     "Professor & Head of Dermatology. Expert in clinical and procedural dermatology with specialization in autoimmune skin disorders.",
     "DrGhanshyamVerma.jpg"),

    ("Renu",    "Rattan",    "Dermatology", 20,
     "Professor specializing in contact dermatology, psoriasis, and skin allergy management.",
     "Reema.jpg"),

    ("Ajeet",   "Negi",      "Dermatology", 12,
     "Assistant Professor with expertise in dermato-surgery and laser treatment.",
     "AJEET_NEGI.jpg"),

    ("Sandhya", "Chauhan",   "Dermatology", 10,
     "Assistant Professor specializing in dermatopathology and pediatric skin disorders.",
     "SandhyaChauhan.jpg"),

    # OPHTHALMOLOGY ───────────────────────────────────────────
    ("Ram Lal", "Sharma",    "Ophthalmology", 32,
     "Professor & Head of Ophthalmology. Renowned for cataract microsurgery, glaucoma management, and corneal transplantation.",
     "RAM SHARMA.jpeg"),

    ("Vinod",   "Kashyap",   "Ophthalmology", 22,
     "Professor specializing in vitreoretinal surgery and diabetic eye disease.",
     "vinod kashyap.jpeg"),

    ("Parveen", "Panwar",    "Ophthalmology", 18,
     "Associate Professor with expertise in pediatric ophthalmology and squint correction.",
     "praveen panwar.jpeg"),

    ("Vinay",   "Gupta",     "Ophthalmology", 14,
     "Associate Professor specializing in cornea, ocular surface diseases, and refractive surgery.",
     "Vinay Gupta.JPG"),

    # ORTHOPEDICS ─────────────────────────────────────────────
    ("Vineet",  "Aggarwal",  "Orthopedics", 28,
     "Professor & Head of Orthopedics. Expert in joint replacement surgery, complex trauma, and spine surgery.",
     "v2.bmp"),

    ("Desh Raj","Chandel",   "Orthopedics", 24,
     "Professor specializing in pelvi-acetabular fractures and limb reconstruction.",
     "Desh Raj Chandel.jpg"),

    ("Rajesh",  "Sood",      "Orthopedics", 22,
     "Professor with expertise in pediatric orthopedics and sports medicine.",
     "rajeshsood.jpeg"),

    ("Sandeep", "Kashyap",   "Orthopedics", 16,
     "Associate Professor specializing in arthroscopic surgery and knee reconstruction.",
     "drsk.jpeg"),

    # PEDIATRICS ──────────────────────────────────────────────
    ("Parveen", "Bhardwaj",  "Pediatrics", 26,
     "Professor & Head of Pediatrics. Expert in neonatology, pediatric intensive care, and childhood infectious diseases.",
     None),

    ("Ashwani", "Sood",      "Pediatrics", 20,
     "Professor specializing in pediatric neurology and developmental disorders.",
     None),

    ("Neeraj",  "Kumar",     "Pediatrics", 16,
     "Professor with expertise in pediatric endocrinology and metabolic diseases.",
     None),

    ("Soma",    "Devi",      "Pediatrics", 12,
     "Assistant Professor specializing in neonatal care and pediatric emergency medicine.",
     None),

    # RADIOTHERAPY ────────────────────────────────────────────
    ("Manish",  "Gupta",     "Radiotherapy", 24,
     "Professor & Head of Radiotherapy. Expert in radiation oncology with specialization in head-neck cancers and stereotactic treatments.",
     None),

    ("Vikas",   "Fotedar",   "Radiotherapy", 18,
     "Professor specializing in brachytherapy and gynecological oncology.",
     None),

    ("Siddharth","Vats",     "Radiotherapy", 14,
     "Associate Professor with expertise in intensity-modulated radiotherapy (IMRT) and image-guided techniques.",
     None),

    ("Purnima", "Thakur",    "Radiotherapy", 10,
     "Assistant Professor specializing in palliative radiotherapy and breast cancer treatment.",
     None),

    # EMERGENCY MEDICINE ──────────────────────────────────────
    ("Jitender Kumar","Mokta", "Emergency Medicine", 22,
     "Professor specializing in emergency and critical care medicine with expertise in trauma resuscitation.",
     None),

    ("Vivek",   "Chauhan",   "Emergency Medicine", 16,
     "Associate Professor with expertise in pre-hospital care and mass casualty management.",
     None),

    ("Rajiv",   "Kundlas",   "Emergency Medicine", 12,
     "Assistant Professor specializing in toxicology and emergency airway management.",
     None),

    ("Balbir",  "Singh",     "Emergency Medicine", 18,
     "Professor with expertise in cardiac emergencies and emergency ultrasound.",
     None),
]


def download_photo(filename, save_as):
    """Download a real photo from IGMC site."""
    if not filename:
        return None
    url = BASE_URL + filename
    dest = MEDIA_DIR / save_as
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(dest, "wb") as f:
                f.write(resp.read())
        print(f"  ✔ Downloaded: {filename} → {save_as}")
        return f"doctors/{save_as}"
    except Exception as e:
        print(f"  ✘ Failed {filename}: {e}")
        return None


def make_username(first, last):
    u = f"dr.{first.split()[0].lower()}_{last.lower()}"
    u = re.sub(r'[^a-z0-9_]', '', u)[:30]
    # make unique
    base, suffix = u, 2
    while User.objects.filter(username=base).exists():
        base = u[:27] + str(suffix)
        suffix += 1
    return base


print("\n🏥 Starting IGMC Doctor Seeder...")
print(f"   Media directory: {MEDIA_DIR}")

created = 0
skipped = 0

for (first, last, spec, exp, bio, photo_file) in DOCTORS:
    full_name = f"Dr. {first} {last}"
    print(f"\n→ {full_name} | {spec}")

    # Check if already exists
    existing = Doctor.objects.filter(
        user__first_name=first,
        user__last_name=last,
        specialization=spec
    ).first()
    if existing:
        print(f"  ⚠ Already exists (ID:{existing.pk}), skipping.")
        skipped += 1
        continue

    # Download photo
    photo_path = None
    if photo_file:
        ext = Path(photo_file).suffix.lower()
        safe_name = f"{first.split()[0]}_{last}_{spec.split()[0]}{ext}".replace(" ", "_").lower()
        photo_path = download_photo(photo_file, safe_name)

    # Create User
    username = make_username(first, last)
    password = f"doc{last.lower()[:4]}2025"
    user = User.objects.create_user(
        username=username,
        first_name=first,
        last_name=last,
        email=f"{username}@hospinex.in",
        password=password,
        is_staff=True,
    )

    # Create Doctor profile
    doc = Doctor.objects.create(
        user=user,
        specialization=spec,
        experience=exp,
        bio=bio,
    )

    if photo_path:
        doc.photo = photo_path
        doc.save()

    print(f"  ✅ Created: {full_name} | username={username} | photo={'yes' if photo_path else 'no'}")
    created += 1

print(f"\n{'='*50}")
print(f"✅ Done! Created: {created} | Skipped (already existed): {skipped}")
print(f"   Total doctors now: {Doctor.objects.count()}")
