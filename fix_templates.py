import os
import glob
import re

files_to_fix = glob.glob('d:/hospital/templates/**/*.html', recursive=True)

unsplash_pattern = re.compile(r'https://images\.unsplash\.com/[^\'\"\?]+(?:\?[^\'\"]*)?')

for f in files_to_fix:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    dirty = False
    
    # 1. Replace all unsplash with bg1.png as base
    if 'unsplash.com' in content:
        content = unsplash_pattern.sub('{% static "images/gallery/bg1.png" %}', content)
        dirty = True
        
    # 2. Add missing {% load static %} near the top if the file has {% extends "base.html" %} 
    # but misses {% load static %}
    if '{% extends "base.html" %}' in content and '{% load static %}' not in content:
        content = content.replace('{% extends "base.html" %}', '{% extends "base.html" %}\n{% load static %}')
        dirty = True

    # 3. Apply specific home.html enhancements from screenshots
    if 'home.html' in f:
        # The badge
        old_badge = '''<div class="experience-badge">
                    <span>50+</span>
                    <p>Years of Legacy</p>
                </div>'''
        new_badge = '''<div class="experience-badge" style="background: rgba(46, 125, 50, 0.95); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.3); border-radius: 18px; padding: 25px 35px;">
                    <span>50+</span><br><small style="font-weight: 700; font-size: 16px; letter-spacing: 1px;">YEARS OF</small><br><strong style="font-size: 20px;">LEGACY</strong>
                </div>'''
        if old_badge in content:
            content = content.replace(old_badge, new_badge)
            dirty = True
            
        old_img = '''<img src="{% static 'images/gallery/hospital.jpg' %}" alt="Civil Hospital Ghumarwin Facility" style="width:100%; height:100%; object-fit:cover; border-radius:20px;">'''
        new_img = '''<img src="{% static 'images/gallery/ghumarwin_actual_entrance.png' %}" alt="Civil Hospital Ghumarwin Entrance" style="width:100%; height:100%; object-fit:cover; border-radius:18px; filter: contrast(1.1) brightness(1.05);">'''
        if old_img in content:
            content = content.replace(old_img, new_img)
            dirty = True
            
        # Fix the 4 gallery cards (since unsplash turned them all to bg1.png)
        if 'gallery-card' in content:
            replacements = [
                "{% static 'images/gallery/ghumarwin_civil_2.jpeg' %}",
                "{% static 'images/gallery/ghumarwin_civil_4.jpeg' %}",
                "{% static 'images/gallery/ghumarwin_civil_6.jpeg' %}",
                "{% static 'images/gallery/ghumarwin_civil_8.jpeg' %}"
            ]
            for rep in replacements:
                content = content.replace('{% static "images/gallery/bg1.png" %}', rep, 1)
            dirty = True
            
        # Fix department images 
        if 'department-card' in content:
            dept_replacements = [
                "{% static 'images/depts/dept_generalsurgery.png' %}",
                "{% static 'images/gallery/bg2.png' %}",
                "{% static 'images/depts/dept_orthopedics.png' %}",
                "{% static 'images/depts/dept_pediatrics.png' %}",
                "{% static 'images/depts/dept_ophthalmology.png' %}",
                "{% static 'images/gallery/ghumarwin_civil_9.jpeg' %}",
                "{% static 'images/gallery/ghumarwin_civil_10.jpeg' %}"
            ]
            for rep in dept_replacements:
                content = content.replace('{% static "images/gallery/bg1.png" %}', rep, 1)
            dirty = True
            
    # 4. Specific gallery.html replacements
    if 'gallery.html' in f:
        reps = {
            'g1.jpg': 'ghumarwin_civil_1.jpeg',
            'g2.jpg': 'ghumarwin_civil_2.jpeg',
            'g3.jpg': 'ghumarwin_civil_3.jpeg',
            'g4.jpg': 'ghumarwin_civil_4.jpeg',
            'g5.jpg': 'ghumarwin_civil_5.jpeg',
            'g6.jpg': 'ghumarwin_civil_6.jpeg',
            'g7.jpg': 'ghumarwin_civil_7.jpeg',
            'g8.jpg': 'xray_corridor.png'
        }
        for old, new in reps.items():
            if old in content:
                content = content.replace(old, new)
                dirty = True

    if dirty:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fixed {f}")
