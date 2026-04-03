import urllib.request
import re
import os

BASE = "http://www.igmcshimla.edu.in"
pages = {
    "Anesthesia":         "/meta/anesth.jsp",
    "General Surgery":    "/meta/Surgery.jsp",
    "Dermatology":        "/meta/Dermatology.jsp",
    "Ophthalmology":      "/meta/Eye.jsp",
    "Orthopedics":        "/meta/ortho.jsp",
    "Pediatrics":         "/meta/Paediatrics.jsp",
    "Radiotherapy":       "/meta/radiotherapy.jsp",
    "Emergency Medicine": "/meta/Emergency.jsp",
}

for dept, path in pages.items():
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8", "ignore")
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
        print("[OK] " + dept + " | imgs: " + str(imgs[:8]))
    except Exception as e:
        print("[FAIL] " + dept + ": " + str(e))
