import urllib.request
import re
import os
import sys

BASE = "http://www.igmcshimla.edu.in"
MEDIA_DIR = os.path.join(os.path.dirname(__file__), "media", "doctors")
os.makedirs(MEDIA_DIR, exist_ok=True)

pages = {
    "Anesthesia":         "/meta/anesth.jsp",
    "General Surgery":    "/meta/Surgery.jsp",
    "Dermatology":        "/meta/Dermatology.jsp",
    "Ophthalmology":      "/meta/Eye.jsp",
    "Orthopedics":        "/meta/ortho.jsp",
    "Pediatrics":         "/meta/Paediatrics.jsp",
    "Radiotherapy":       "/meta/radiotherapy.jsp",
}

all_data = {}

for dept, path in pages.items():
    url = BASE + path
    print("=" * 60)
    print("DEPT:", dept)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read().decode("utf-8", "ignore")

        # Find all img src values
        imgs = re.findall(r'src=["\']([^"\']+)["\']', html, re.I)
        # Filter only doctor/avatar images (not banner/logo)
        doctor_imgs = [i for i in imgs if "avatar" in i.lower() or "doctor" in i.lower() or "faculty" in i.lower() or "photo" in i.lower() or ".jpg" in i.lower() or ".jpeg" in i.lower() or ".png" in i.lower()]
        doctor_imgs = [i for i in doctor_imgs if "banner" not in i.lower() and "logo" not in i.lower() and "icon" not in i.lower() and "flag" not in i.lower()]

        print("  All imgs:", imgs[:3])
        print("  Doctor imgs:", doctor_imgs[:10])

        # Also extract names from table rows 
        # Look for table cells with names
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.I | re.S)
        for row in rows[:30]:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row, re.I | re.S)
            if len(cells) >= 2:
                name_txt = re.sub(r'<[^>]+>', '', cells[0]).strip()
                if name_txt and len(name_txt) > 3 and ("Dr." in name_txt or "Prof" in name_txt or "Dr " in name_txt):
                    desig = re.sub(r'<[^>]+>', '', cells[1]).strip() if len(cells) > 1 else ""
                    print(f"  NAME: {name_txt[:60]} | DESIG: {desig[:50]}")

        all_data[dept] = doctor_imgs

    except Exception as e:
        print("  FAILED:", e)
        all_data[dept] = []

print("\n\n=== SUMMARY OF IMAGE URLs ===")
for dept, imgs in all_data.items():
    print(f"\n{dept}:")
    for img in imgs[:8]:
        full = img if img.startswith("http") else BASE + "/" + img.lstrip("./")
        print(f"  {full}")
