from django.contrib import admin
from .models import Customer,Appointment,DoctorRadiologist,DoctorRadiologistNotification,RadiologistDoctor,RadiologistDoctorNotification,Recomendation,DoctorSpecialistData,DoctorSpecialistNotification,DoctorSpecialistRequest,SpecialistDoctorNotification,SpecialistDoctorRecommendation,SpecialistDoctorResponse,MedicalRecord

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'gender', 'city','role']
    list_per_page=10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']  
    search_fields = ['user__first_name', 'user__last_name']






