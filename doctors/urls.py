from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # HOME
    # =========================
    path("", views.home, name="home"),

    # =========================
    # DOCTORS
    # =========================
    path("doctors/", views.doctor_list, name="doctor_list"),
    path("doctors/<int:doctor_id>/", views.doctor_detail, name="doctor_detail"),

    # =========================
    # APPOINTMENTS
    # =========================
    path("book/<int:user_id>/", views.book_appointment, name="book_appointment"),
    path("appointment/success/<int:appointment_id>/", views.appointment_success, name="appointment_success"),

    # =========================
    # DOCTOR PANEL
    # =========================
    path("doctor/login/", views.doctor_login, name="doctor_login"),
    path("doctor/dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
    path("doctor/next-patient/", views.next_patient, name="next_patient"),
    path("doctor/complete/<int:appointment_id>/", views.mark_completed, name="mark_completed"),
    # urls.py
path('doctor/emergency/resolve/<int:emergency_id>/', views.resolve_emergency, name='resolve_emergency'),
    path("doctor/notification/<int:appointment_id>/", views.view_notification_appointment, name="view_notification_appointment"),

    # =========================
    # PATIENT PANEL
    # =========================
    path("patient/login/", views.patient_login, name="patient_login"),
    path("patient/dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path("patient/cancel/<int:appointment_id>/", views.cancel_appointment, name="cancel_appointment"),

    # =========================
    # RECEPTIONIST PANEL
    # =========================
    path("receptionist/login/", views.receptionist_login, name="receptionist_login"),
    path("receptionist/dashboard/", views.receptionist_dashboard, name="receptionist_dashboard"),
    path("receptionist/logout/", views.receptionist_logout, name="receptionist_logout"),
    path("receptionist/appointments/", views.receptionist_appointments, name="receptionist_appointments"),
    path("receptionist/add/", views.add_appointment, name="add_appointment"),
    path("receptionist/emergency/", views.send_emergency, name="send_emergency"),

    # =========================
    # ADMIN ACTIONS
    # =========================
    path("delete-all/", views.delete_all_appointments, name="delete_all_appointments"),
    path("delete-selected/", views.delete_selected_appointments, name="delete_selected_appointments"),

    # =========================
    # STATIC PAGES
    # =========================
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("gallery/", views.gallery, name="gallery"),
    path("departments/", views.departments_view, name="departments_page"),

    # =========================
    # LOGOUT
    # =========================
    path("logout/", views.logout_view, name="logout"),
    path('doctor-logout/', views.doctor_logout_view, name='doctor_logout'),
    path('patient-logout/', views.patient_logout_view, name='patient_logout'),
]