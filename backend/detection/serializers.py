from .models import Customer,Appointment,Notification,DoctorRadiologist,DoctorRadiologistNotification,RadiologistDoctor,RadiologistDoctorNotification,MedicalRecord,Recomendation,DoctorSpecialistRequest,DoctorSpecialistNotification,SpecialistDoctorResponse,SpecialistDoctorNotification,DoctorSpecialistData,SpecialistDoctorRecommendation,DoctorPatientMessage,DoctorPatientMessageNotification,SegmentedImagePredictionTotal
from rest_framework import serializers
import base64

from django.conf import settings
from drf_extra_fields.fields import Base64ImageField  # type: ignore # You need to install drf-extra-fields
from core.models import User
class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    username=serializers.CharField(source='user.username',read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'first_name', 'last_name','username', 'phone', 'city', 'gender', 'bio', 'image','role']
class RecomendationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Recomendation
        fields='__all__'
class SpecialistDoctorRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model=SpecialistDoctorRecommendation
        fields='__all__'

class DoctorSpecialistRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorSpecialistRequest
        fields='__all__'
class DoctorPatientMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=DoctorPatientMessage
        fields='__all__'

class SpecialistDoctorResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=SpecialistDoctorResponse
        fields='__all__'


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.SerializerMethodField()
    patient_last_name = serializers.SerializerMethodField()
    patient_username = serializers.SerializerMethodField()
    patient_city = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    class Meta:
        model=MedicalRecord
        fields=['id','doctor','patient','patient_first_name','patient_last_name','patient_city','patient_phone','patient_username','weight','systolic_blood_pressure','diastolic_blood_pressure','blood_sugar_level','heart_rate','cholesterol_level','doctor_notes']
    def get_patient_first_name(self, obj):
        # Access the patient object from the appointment instance and get the first name
        patient = obj.patient
        if patient:
            return patient.first_name
        return None
    def get_patient_last_name(self, obj):
        patient = obj.patient
        if patient:
            return patient.last_name
        return None
    def get_patient_username(self, obj):
        patient = obj.patient
        if patient:
            return patient.username
        return None
    def get_patient_city(self, obj):
        patient = obj.patient
        if patient and hasattr(patient, 'customer'):
            return patient.customer.city
        return None

    def get_patient_phone(self, obj):
        patient = obj.patient
        if patient and hasattr(patient, 'customer'):
            return patient.customer.phone
        return None
    
class CustomCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['city', 'phone']


class RadiologistDoctorSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.SerializerMethodField()
    patient_last_name = serializers.SerializerMethodField()
    patient_city = serializers.SerializerMethodField()
    patient_systolic_blood_pressure = serializers.SerializerMethodField()
    patient_diastolic_blood_pressure = serializers.SerializerMethodField()
    patient_blood_sugar_level = serializers.SerializerMethodField()
    patient_weight = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_heart_rate=serializers.SerializerMethodField()
    patient_cholesterol_level=serializers.SerializerMethodField()
    doctor_notes=serializers.SerializerMethodField()
    class Meta:
        model = RadiologistDoctor
        fields = [
            'id', 'doctor', 'image', 'patient', 'radiologist', 'prediction','recommendation',
            'patient_first_name', 'patient_last_name', 'patient_city', 'patient_phone',
            'patient_weight', 'patient_systolic_blood_pressure', 'patient_diastolic_blood_pressure', 'patient_blood_sugar_level','patient_heart_rate','patient_cholesterol_level','doctor_notes'
        ]

    def get_patient_first_name(self, obj):
        patient = obj.patient
        return patient.first_name if patient else None

    def get_patient_last_name(self, obj):
        patient = obj.patient
        return patient.last_name if patient else None

    def get_patient_city(self, obj):
        patient = obj.patient
        if patient and hasattr(patient, 'customer'):
            return patient.customer.city
        return None

    def get_patient_phone(self, obj):
        patient = obj.patient
        if patient and hasattr(patient, 'customer'):
            return patient.customer.phone
        return None

    def get_patient_weight(self, obj):
        return self._get_medical_record_field(obj, 'weight')

    def get_patient_systolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'systolic_blood_pressure')

    def get_patient_diastolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'diastolic_blood_pressure')

    def get_patient_blood_sugar_level(self, obj):
        return self._get_medical_record_field(obj, 'blood_sugar_level')
    def get_patient_heart_rate(self, obj):
        return self._get_medical_record_field(obj, 'heart_rate')
    def get_patient_cholesterol_level(self, obj):
        return self._get_medical_record_field(obj, 'cholesterol_level')
    def get_doctor_notes(self, obj):
        return self._get_medical_record_field(obj, 'doctor_notes')

    def _get_medical_record_field(self, obj, field):
        try:
            medical_record = MedicalRecord.objects.filter(patient=obj.patient).order_by('-id').first()
            if medical_record:
                return getattr(medical_record, field)
            else:
                return None
        except MedicalRecord.DoesNotExist:
            return None











class AppointmentSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.SerializerMethodField()
    patient_last_name = serializers.SerializerMethodField()
    patient_city = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_systolic_blood_pressure = serializers.SerializerMethodField()
    patient_diastolic_blood_pressure = serializers.SerializerMethodField()
    patient_blood_sugar_level = serializers.SerializerMethodField()
    patient_weight = serializers.SerializerMethodField()
    patient_id = serializers.IntegerField()
    specialist_id = serializers.IntegerField()

    class Meta:
        model = Appointment
        fields = [
            'id', 'appointment_datetime', 'notes', 'patient_id', 'specialist_id',
            'patient_first_name', 'patient_last_name', 'patient_city', 'patient_phone',
            'patient_weight', 'patient_systolic_blood_pressure', 
            'patient_diastolic_blood_pressure', 'patient_blood_sugar_level'
        ]

    def get_patient_first_name(self, obj):
        patient = obj.patient
        if patient:
            return patient.first_name
        return None

    def get_patient_last_name(self, obj):
        patient = obj.patient
        if patient:
            return patient.last_name
        return None

    def get_patient_city(self, obj):
        patient = obj.patient
        if patient and hasattr(patient, 'customer'):
            return patient.customer.city
        return None

    def get_patient_phone(self, obj):
        patient = obj.patient
        if patient and hasattr(patient, 'customer'):
            return patient.customer.phone
        return None

    def get_patient_weight(self, obj):
        return self._get_medical_record_field(obj, 'weight')

    def get_patient_systolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'systolic_blood_pressure')

    def get_patient_diastolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'diastolic_blood_pressure')

    def get_patient_blood_sugar_level(self, obj):
        return self._get_medical_record_field(obj, 'blood_sugar_level')

    def _get_medical_record_field(self, obj, field):
        medical_record = MedicalRecord.objects.filter(patient=obj.patient).order_by('-id').first()
        if medical_record is not None:
            return getattr(medical_record, field)
        return None

class GetSpecialistSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.SerializerMethodField()
    patient_last_name = serializers.SerializerMethodField()
    patient_city = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    # patient_systolic_blood_pressure=serializers.SerializerMethodField()
    # patient_diastolic_blood_pressure=serializers.SerializerMethodField()
    # patient_blood_sugar_level=serializers.SerializerMethodField()
    # patient_weight=serializers.SerializerMethodField()
    # # patient_document=serializers.SerializerMethodField()
    patient_id=serializers.IntegerField()
    specialist_id=serializers.IntegerField()
    
    class Meta:
        model = Appointment
        fields = ['id', 'appointment_datetime', 'notes', 'patient_id', 'specialist_id', 'patient_first_name', 'patient_last_name', 'patient_city', 'patient_phone']
    def get_patient_first_name(self, obj):
        # Access the patient object from the appointment instance and get the first name
        specialist = obj.specialist
        if specialist:
            return specialist.first_name
        return None
    def get_patient_last_name(self, obj):
        # Access the patient object from the appointment instance and get the last name
        specialist = obj.specialist
        if specialist:
            return specialist.last_name
        return None
    def get_patient_city(self, obj):
        specialist = obj.specialist
        if specialist and hasattr(specialist, 'customer'):
            return specialist.customer.city
        return None
    def get_patient_phone(self, obj):
        specialist = obj.specialist
        if specialist and hasattr(specialist, 'customer'):
            return specialist.customer.phone
        return None
class DoctorRadiologistSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.SerializerMethodField()
    patient_last_name = serializers.SerializerMethodField()
    patient_city = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_systolic_blood_pressure = serializers.SerializerMethodField()
    patient_diastolic_blood_pressure = serializers.SerializerMethodField()
    patient_blood_sugar_level = serializers.SerializerMethodField()
    patient_weight = serializers.SerializerMethodField()
    patient_heart_rate = serializers.SerializerMethodField()
    patient_cholesterol_level = serializers.SerializerMethodField()
    doctor_notes = serializers.SerializerMethodField()
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    radiologist_id = serializers.IntegerField()

    class Meta:
        model = DoctorRadiologist
        fields = [
            'id', 'notes', 'patient_id', 'doctor_id', 'radiologist_id', 
            'patient_first_name', 'patient_last_name', 'patient_city', 'patient_phone',
            'patient_weight', 'patient_systolic_blood_pressure', 
            'patient_diastolic_blood_pressure', 'patient_blood_sugar_level', 
            'patient_heart_rate', 'patient_cholesterol_level', 'doctor_notes'
        ]

    def get_patient_first_name(self, obj):
        return obj.patient.first_name if obj.patient else None

    def get_patient_last_name(self, obj):
        return obj.patient.last_name if obj.patient else None

    def get_patient_city(self, obj):
        return obj.patient.customer.city if obj.patient and hasattr(obj.patient, 'customer') else None

    def get_patient_phone(self, obj):
        return obj.patient.customer.phone if obj.patient and hasattr(obj.patient, 'customer') else None

    def get_patient_weight(self, obj):
        return self._get_medical_record_field(obj, 'weight')

    def get_patient_systolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'systolic_blood_pressure')

    def get_patient_diastolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'diastolic_blood_pressure')

    def get_patient_blood_sugar_level(self, obj):
        return self._get_medical_record_field(obj, 'blood_sugar_level')

    def get_patient_heart_rate(self, obj):
        return self._get_medical_record_field(obj, 'heart_rate')

    def get_patient_cholesterol_level(self, obj):
        return self._get_medical_record_field(obj, 'cholesterol_level')

    def get_doctor_notes(self, obj):
        return self._get_medical_record_field(obj, 'doctor_notes')

    def _get_medical_record_field(self, obj, field):
        medical_record = MedicalRecord.objects.filter(patient=obj.patient).order_by('-id').first()
        if medical_record is not None:
            return getattr(medical_record, field)
        return None

# class DoctorSpecialistDataSerializer(serializers.ModelSerializer):
#     patient_first_name = serializers.SerializerMethodField()
#     patient_last_name = serializers.SerializerMethodField()
#     patient_city = serializers.SerializerMethodField()
#     patient_phone = serializers.SerializerMethodField()
#     patient_systolic_blood_pressure = serializers.SerializerMethodField()
#     patient_diastolic_blood_pressure = serializers.SerializerMethodField()
#     patient_blood_sugar_level = serializers.SerializerMethodField()
#     patient_weight = serializers.SerializerMethodField()
#     patient_heart_rate=serializers.SerializerMethodField()
#     patient_cholesterol_level=serializers.SerializerMethodField()
#     doctor_notes=serializers.SerializerMethodField()
#     patient_model_prediction=serializers.SerializerMethodField()
#     patient_radiologist_note=serializers.SerializerMethodField()
#     patient_model_image=serializers.SerializerMethodField()
#     patient_id=serializers.IntegerField()
#     doctor_id=serializers.IntegerField()
#     specialist_id=serializers.IntegerField()
#     class Meta:
#         model = DoctorSpecialistData
#         fields = [
#             'id', 'message','patient_id', 'doctor_id', 'specialist_id', 
#             'patient_first_name', 'patient_last_name', 'patient_city', 'patient_phone',
#             'patient_weight', 'patient_systolic_blood_pressure', 
#             'patient_diastolic_blood_pressure', 'patient_blood_sugar_level','patient_heart_rate','patient_cholesterol_level','doctor_notes','patient_model_prediction','patient_radiologist_note','patient_model_image'
#         ]

#     def get_patient_first_name(self, obj):
#         return obj.patient.first_name if obj.patient else None
#     def get_patient_last_name(self, obj):
#         return obj.patient.last_name if obj.patient else None
#     def get_patient_city(self, obj):
#         return obj.patient.customer.city if obj.patient and hasattr(obj.patient, 'customer') else None
#     def get_patient_phone(self, obj):
#         return obj.patient.customer.phone if obj.patient and hasattr(obj.patient, 'customer') else None
#     def get_patient_weight(self, obj):
#         return self._get_medical_record_field(obj, 'weight')
#     def get_patient_systolic_blood_pressure(self, obj):
#         return self._get_medical_record_field(obj, 'systolic_blood_pressure')

#     def get_patient_diastolic_blood_pressure(self, obj):
#         return self._get_medical_record_field(obj, 'diastolic_blood_pressure')

#     def get_patient_blood_sugar_level(self, obj):
#         return self._get_medical_record_field(obj, 'blood_sugar_level')
#     def get_patient_heart_rate(self, obj):
#         return self._get_medical_record_field(obj, 'heart_rate')
#     def get_patient_cholesterol_level(self, obj):
#         return self._get_medical_record_field(obj, 'cholesterol_level')
#     def get_doctor_notes(self, obj):
#         return self._get_medical_record_field(obj, 'doctor_notes')
#     def get_patient_model_prediction(self, obj):
#         return self._get_radiologist_field(obj, 'prediction')
#     def get_patient_model_image(self, obj):
#         return self._get_radiologist_field(obj, 'image')

#     def get_patient_radiologist_note(self, obj):
#         return self._get_radiologist_field(obj, 'recommendation')
#     def _get_medical_record_field(self, obj, field):
#         try:
#             medical_record = MedicalRecord.objects.filter(patient=obj.patient).order_by('-id').first()
#             return getattr(medical_record, field)
#         except MedicalRecord.DoesNotExist:
#             return None
#     def _get_radiologist_field(self, obj, field):
#         try:
#             radiologist_data = RadiologistDoctor.objects.filter(patient=obj.patient).order_by('-id').first()
#             return getattr(radiologist_data, field)
#         except (DoctorRadiologist.DoesNotExist,DoctorRadiologist.DoesNotExist, UnicodeEncodeError):
#             return None






class DoctorSpecialistDataSerializer(serializers.ModelSerializer):
    patient_first_name = serializers.SerializerMethodField()
    patient_last_name = serializers.SerializerMethodField()
    patient_city = serializers.SerializerMethodField()
    patient_phone = serializers.SerializerMethodField()
    patient_systolic_blood_pressure = serializers.SerializerMethodField()
    patient_diastolic_blood_pressure = serializers.SerializerMethodField()
    patient_blood_sugar_level = serializers.SerializerMethodField()
    patient_weight = serializers.SerializerMethodField()
    patient_heart_rate = serializers.SerializerMethodField()
    patient_cholesterol_level = serializers.SerializerMethodField()
    doctor_notes = serializers.SerializerMethodField()
    patient_model_prediction = serializers.SerializerMethodField()
    patient_model_image=serializers.SerializerMethodField()
    patient_radiologist_note = serializers.SerializerMethodField()
    patient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    specialist_id = serializers.IntegerField()

    class Meta:
        model = DoctorSpecialistData
        fields = [
            'id', 'message', 'patient_id', 'doctor_id', 'specialist_id',
            'patient_first_name', 'patient_last_name', 'patient_city', 'patient_phone',
            'patient_weight', 'patient_systolic_blood_pressure',
            'patient_diastolic_blood_pressure', 'patient_blood_sugar_level', 'patient_heart_rate',
            'patient_cholesterol_level', 'doctor_notes', 'patient_model_prediction', 'patient_radiologist_note','patient_model_image'
        ]

    def get_patient_first_name(self, obj):
        return obj.patient.first_name if obj.patient else None

    def get_patient_last_name(self, obj):
        return obj.patient.last_name if obj.patient else None

    def get_patient_city(self, obj):
        return obj.patient.customer.city if obj.patient and hasattr(obj.patient, 'customer') else None

    def get_patient_phone(self, obj):
        return obj.patient.customer.phone if obj.patient and hasattr(obj.patient, 'customer') else None

    def get_patient_weight(self, obj):
        return self._get_medical_record_field(obj, 'weight')

    def get_patient_systolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'systolic_blood_pressure')

    def get_patient_diastolic_blood_pressure(self, obj):
        return self._get_medical_record_field(obj, 'diastolic_blood_pressure')

    def get_patient_blood_sugar_level(self, obj):
        return self._get_medical_record_field(obj, 'blood_sugar_level')

    def get_patient_heart_rate(self, obj):
        return self._get_medical_record_field(obj, 'heart_rate')

    def get_patient_cholesterol_level(self, obj):
        return self._get_medical_record_field(obj, 'cholesterol_level')

    def get_doctor_notes(self, obj):
        return self._get_medical_record_field(obj, 'doctor_notes')

    def get_patient_model_image(self, obj):
        # Get the image field URL
        try:
            radiologist_data = RadiologistDoctor.objects.filter(patient=obj.patient).order_by('-id').first()
            if radiologist_data and radiologist_data.image:
                return radiologist_data.image.url
            return None
        except (RadiologistDoctor.DoesNotExist, AttributeError):
            return None

    def get_patient_radiologist_note(self, obj):
        return self._get_radiologist_field(obj, 'recommendation')
    def get_patient_model_prediction(self, obj):
        return self._get_radiologist_field(obj, 'prediction')

    def _get_medical_record_field(self, obj, field):
        try:
            medical_record = MedicalRecord.objects.filter(patient=obj.patient).order_by('-id').first()
            return getattr(medical_record, field, None)
        except MedicalRecord.DoesNotExist:
            return None

    def _get_radiologist_field(self, obj, field):
        try:
            radiologist_data = RadiologistDoctor.objects.filter(patient=obj.patient).order_by('-id').first()
            return getattr(radiologist_data, field, None)
        except (RadiologistDoctor.DoesNotExist, AttributeError):
            return None














class NotificationSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()
    specialist_id = serializers.IntegerField()
    message = serializers.CharField( read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'recipient_id', 'specialist_id', 'message', 'created_at']

class DoctorRadiologistNotificationSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    message = serializers.CharField( read_only=True)
    class Meta:
        model = DoctorRadiologistNotification
        fields = ['id', 'recipient_id', 'doctor_id', 'message','read', 'created_at']
class SpecialistDoctorNotificationSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()
    specialist_id = serializers.IntegerField()
    message = serializers.CharField( read_only=True)
    class Meta:
        model = SpecialistDoctorNotification
        fields = ['id', 'recipient_id', 'specialist_id', 'message','read', 'created_at']


class DoctorSpecialistNotificationSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    message = serializers.CharField( read_only=True)
    class Meta:
        model = DoctorSpecialistNotification
        fields = ['id', 'recipient_id', 'doctor_id', 'message', 'created_at','read']
class DoctorPatientMessageNotificationSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()
    doctor_id = serializers.IntegerField()
    message = serializers.CharField( read_only=True)
    class Meta:
        model = DoctorPatientMessageNotification
        fields = ['id', 'recipient_id', 'doctor_id', 'message', 'created_at','read']

class RadiologistDoctorNotificationSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()
    radiologist_id = serializers.IntegerField()
    message = serializers.CharField( read_only=True)
    class Meta:
        model = RadiologistDoctorNotification
        fields = ['id', 'recipient_id', 'radiologist_id', 'message', 'read', 'created_at']




class SegmentedImagePredictionTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SegmentedImagePredictionTotal
        fields = ['id', 'image', 'segmentation_result', 'classification_result']
        read_only_fields = ['id', 'segmentation_result', 'classification_result']



