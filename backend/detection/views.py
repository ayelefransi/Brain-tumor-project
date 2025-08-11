from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
import time
import logging
import os
import cv2
import numpy as np
from socket import gaierror
from smtplib import SMTPException
from rest_framework import status
from django.core.mail import send_mail
logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Customer,Appointment,Notification,Recomendation,DoctorRadiologist,DoctorRadiologistNotification,RadiologistDoctor,RadiologistDoctorNotification,MedicalRecord,DoctorSpecialistRequest,DoctorSpecialistNotification,SpecialistDoctorNotification,SpecialistDoctorResponse,DoctorSpecialistData,SpecialistDoctorRecommendation,DoctorPatientMessage,DoctorPatientMessageNotification
from .serializers import CustomerSerializer,AppointmentSerializer,NotificationSerializer,RecomendationSerializer,DoctorRadiologistSerializer,DoctorRadiologistNotificationSerializer,RadiologistDoctorSerializer,RadiologistDoctorNotificationSerializer,MedicalRecordSerializer,DoctorSpecialistRequestSerializer,SpecialistDoctorResponseSerializer,DoctorSpecialistDataSerializer,SpecialistDoctorRecommendationSerializer,DoctorSpecialistNotificationSerializer,SpecialistDoctorNotificationSerializer,GetSpecialistSerializer,DoctorPatientMessageSerializer,DoctorPatientMessageNotificationSerializer
from rest_framework.decorators import action
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from tensorflow.keras.models import load_model
from keras.utils import custom_object_scope
from PIL import Image
from django.core.files.storage import FileSystemStorage
from .models import SegmentedImagePredictionTotal
from .serializers import SegmentedImagePredictionTotalSerializer
from .custom_losses import bce_dice_loss
from .custom_metrics import iou_metric


def send_email_with_retry(subject, message, from_email, recipient_list, retries=3, delay=5):
    for i in range(retries):
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return
        except (SMTPException, gaierror) as e:
            logger.warning(f"Attempt {i+1} to send email failed: {e}")
            if i < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                logger.error(f"All {retries} attempts to send email failed")
                raise e  # Raise the exception if all retries fail

class RadiologistDoctorViewSet(ModelViewSet):
    queryset = RadiologistDoctor.objects.select_related('doctor', 'patient', 'radiologist').all()
    serializer_class = RadiologistDoctorSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mriscanimage = serializer.save()
        
        # Retrieve doctor, patient, and radiologist objects
        doctor_id = serializer.validated_data['doctor'].id
        patient_id = serializer.validated_data['patient'].id
        radiologist_id = serializer.validated_data['radiologist'].id
        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        patient = User.objects.get(id=patient_id)
        radiologist = User.objects.get(id=radiologist_id)
        
        # Construct message with patient's first name and last name
        patient_name = f"{patient.first_name} {patient.last_name}"
        message_without_id = f"New Information Upload from Radiologist {radiologist.first_name} {radiologist.last_name} for patient {patient_name}"
        message_with_id = f"{message_without_id} (ID: {mriscanimage.id})"
        
        # Create RadiologistDoctorNotification without ID
        RadiologistDoctorNotification.objects.create(recipient=doctor, radiologist_id=radiologist_id, message=message_with_id)
        
        # Send email notification with retry logic
        sender_email = "fetamasr@gmail.com"
        recipient_email = doctor.email
        try:
            send_email_with_retry(
                'New Information Upload Notification',
                message_without_id,  # Send email without ID
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GetPatientBasedOnRadiologistViewSet(ModelViewSet):
    serializer_class = DoctorRadiologistSerializer
    def get_queryset(self):
        radiologist_id = self.request.query_params.get('radiologist_id')
        if radiologist_id:
            return DoctorRadiologist.objects.filter(radiologist_id=radiologist_id)
        return DoctorRadiologist.objects.none()




class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.select_related('specialist', 'patient').all()
    serializer_class = AppointmentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        
        specialist_id = serializer.validated_data['specialist_id']
        patient_id = serializer.validated_data['patient_id']
        
        User = get_user_model()
        specialist = User.objects.get(id=specialist_id)
        patient = User.objects.get(id=patient_id)
        
        specialist_name = f"{specialist.first_name} {specialist.last_name}"
        patient_name = f"{patient.first_name} {patient.last_name}"
        
        formatted_datetime = serializer.validated_data['appointment_datetime'].strftime('%A, %B %d, %Y at %I:%M %p')
        
        message_without_id = f"New appointment From Specialist {specialist_name} scheduled for you on {formatted_datetime}"
        
        Notification.objects.create(recipient=patient, specialist_id=specialist_id, message=message_without_id)
        
        sender_email = "fetamasr@gmail.com"
        recipient_email = patient.email
        
        try:
            send_email_with_retry(
                'New Appointment Notification From Specialist',
                message_without_id,
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        specialist_id = self.request.query_params.get('specialist_id')
        if specialist_id:
            return Appointment.objects.filter(specialist_id=specialist_id)
        return Appointment.objects.all()

    




class GetAppointementListBasedOnPatientViewSet(ModelViewSet):
    queryset = Appointment.objects.select_related('specialist', 'patient').all()
    serializer_class = GetSpecialistSerializer
    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return Appointment.objects.filter(patient_id=patient_id)
        return Appointment.objects.all()



class DoctorRadiologistViewSet(ModelViewSet):
    queryset = DoctorRadiologist.objects.select_related('doctor', 'patient', 'radiologist').all()
    serializer_class = DoctorRadiologistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor_radiologist = serializer.save()

        doctor_id = serializer.validated_data['doctor_id']
        patient_id = serializer.validated_data['patient_id']
        radiologist_id = serializer.validated_data['radiologist_id']

        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        patient = User.objects.get(id=patient_id)
        radiologist = User.objects.get(id=radiologist_id)

        patient_name = f"{patient.first_name} {patient.last_name}"
        doctor_name = f"{doctor.first_name} {doctor.last_name}"

        message_without_id = f"New Message From Doctor {doctor_name} for patient {patient_name}"
        message_with_id = f"{message_without_id} (ID: {doctor_radiologist.id})"
        DoctorRadiologistNotification.objects.create(recipient=radiologist, doctor_id=doctor_id, message=message_with_id)

        sender_email = "fetamasr@gmail.com"
        recipient_email = radiologist.email

        try:
            send_email_with_retry(
                'New Message Notification From Doctor',
                message_without_id,
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return DoctorRadiologist.objects.filter(patient_id=patient_id)
        return DoctorRadiologist.objects.all()

    






    
class DoctorSpecialistDataViewSet(ModelViewSet):
    queryset = DoctorSpecialistData.objects.select_related('doctor', 'patient', 'specialist').all()
    serializer_class = DoctorSpecialistDataSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctorspecialistdata = serializer.save()
        doctor_id = serializer.validated_data['doctor_id']
        patient_id = serializer.validated_data['patient_id']
        specialist_id = serializer.validated_data['specialist_id']

        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        patient = User.objects.get(id=patient_id)
        specialist = User.objects.get(id=specialist_id)

        doctor_name = f"{doctor.first_name} {doctor.last_name}"
        patient_name = f"{patient.first_name} {patient.last_name}"

        message_without_id = f"New Message From Doctor {doctor_name} for data sending for patient {patient_name}"
        message_with_id = f"{message_without_id} (ID: {doctorspecialistdata.id})"
        DoctorSpecialistNotification.objects.create(recipient=specialist, doctor_id=doctor_id, message=message_with_id)

        sender_email = "fetamasr@gmail.com"
        recipient_email = specialist.email

        try:
            send_email_with_retry(
                'New Message Notification From Doctor',
                message_without_id,
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return DoctorSpecialistData.objects.filter(patient_id=patient_id)
        return DoctorSpecialistData.objects.all()

class GetPatientBasedOnDoctorSpecialistDataViewSet(ModelViewSet):
    serializer_class = DoctorSpecialistDataSerializer
    def get_queryset(self):
        specialist_id = self.request.query_params.get('specialist_id')
        if specialist_id:
            return DoctorSpecialistData.objects.filter(specialist_id=specialist_id)
        return DoctorSpecialistData.objects.none()























class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(recipient_id=doctor_id)
        return queryset
class DoctorRadiologistNotificationViewSet(ModelViewSet):
    queryset = DoctorRadiologistNotification.objects.all()
    serializer_class = DoctorRadiologistNotificationSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        radiologist_id = self.request.query_params.get('radiologist_id')
        if radiologist_id:
            queryset = queryset.filter(recipient_id=radiologist_id)
        return queryset.order_by('-id')
class RadiologistDoctorNotificationViewSet(ModelViewSet):
    queryset = RadiologistDoctorNotification.objects.all()
    serializer_class = RadiologistDoctorNotificationSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(recipient_id=doctor_id)
        return queryset.order_by('-id')
    
class DoctorSpecialistNotificationViewSet(ModelViewSet):
    queryset = DoctorSpecialistNotification.objects.all()
    serializer_class = DoctorSpecialistNotificationSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        specialist_id = self.request.query_params.get('specialist_id')
        read_status = self.request.query_params.get('read')
        if specialist_id and read_status:
            queryset = queryset.filter(recipient_id=specialist_id, read=read_status)
        elif specialist_id:
            queryset = queryset.filter(recipient_id=specialist_id)
        elif read_status:
            queryset = queryset.filter(read=read_status)
        return queryset.order_by('-id')
class DoctorPatientMessageNotificationViewSet(ModelViewSet):
    queryset = DoctorPatientMessageNotification.objects.all()
    serializer_class = DoctorPatientMessageNotificationSerializer
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient_id')
        read_status = self.request.query_params.get('read')
        if patient_id and read_status:
            queryset = queryset.filter(recipient_id=patient_id, read=read_status)
        elif patient_id:
            queryset = queryset.filter(recipient_id=patient_id)
        elif read_status:
            queryset = queryset.filter(read=read_status)
        return queryset.order_by('-id')
class SpecialistDoctorNotificationViewSet(ModelViewSet):
    queryset = SpecialistDoctorNotification.objects.all()
    serializer_class = SpecialistDoctorNotificationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(recipient_id=doctor_id)
        return queryset.order_by('-id')  # Order notifications by ID in descending order



class CustomerViewSet(CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,GenericViewSet):
    queryset=Customer.objects.select_related('user').all()
    serializer_class=CustomerSerializer
    @action(detail=False, methods=['GET'])
    def doctors(self, request):
        doctors = Customer.objects.filter(role='doctor')
        serializer = CustomerSerializer(doctors, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['GET'])
    def specialists(self, request):
        specialists = Customer.objects.filter(role='specialist')
        serializer = CustomerSerializer(specialists, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['GET'])
    def patients(self, request):
        patients = Customer.objects.filter(role='patient')
        serializer = CustomerSerializer(patients, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['GET'])
    def radiologists(self, request):
        radiologists = Customer.objects.filter(role='radiologist')
        serializer = CustomerSerializer(radiologists, many=True)
        return Response(serializer.data)
    @action(detail=False,methods=['GET','PUT'])
    def me(self,request):
        # return self.retrieve(request)
        (customer,created)=Customer.objects.get_or_create(user_id=request.user.id)
        if request.method=='GET':
            serializer=CustomerSerializer(customer)
            return Response(serializer.data)   
        elif request.method=='PUT':
            serializer=CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data) 


















class PatientInfoViewSet(ModelViewSet):
    queryset = Recomendation.objects.select_related('user','doctor').all()
    serializer_class = RecomendationSerializer
    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):
        # Retrieve all recommendations for the current user
        recommendations = Recomendation.objects.filter(user_id=request.user.id)
        if request.method == 'GET':
            # Serialize and return all recommendations
            serializer = RecomendationSerializer(recommendations, many=True)
            return Response(serializer.data)
        elif request.method == 'PUT':
            # Handle PUT request, assuming updating the first recommendation
            if recommendations.exists():
                recommendation = recommendations.first()
                serializer = RecomendationSerializer(recommendation, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"error": "There is no patient info for this user"}, status=status.HTTP_404_NOT_FOUND)






class MedicalRecordViewSet(ModelViewSet):
    serializer_class = MedicalRecordSerializer
    def get_queryset(self):
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            return MedicalRecord.objects.filter(patient__id=patient_id)
        return MedicalRecord.objects.none()  # Return no records if no patient_id is provided
  
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def put(self, request, *args, **kwargs):
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({"detail": "Patient ID not provided."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            medical_record = MedicalRecord.objects.get(patient__id=patient_id)
        except MedicalRecord.DoesNotExist:
            return Response({"detail": "Medical record not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(medical_record, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class GetPatientBasedOnMedicalRecordViewSet(ModelViewSet):
    serializer_class = MedicalRecordSerializer
    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            return MedicalRecord.objects.filter(doctor_id=doctor_id)
        return MedicalRecord.objects.none()





class DoctorSpecialistRequestViewSet(ModelViewSet):
    queryset = DoctorSpecialistRequest.objects.select_related('doctor','specialist').all()
    serializer_class = DoctorSpecialistRequestSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctorrequest = serializer.save()
        
        # Retrieve doctor and specialist objects
        doctor_id = serializer.validated_data['doctor'].id
        specialist_id = serializer.validated_data['specialist'].id
        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        specialist = User.objects.get(id=specialist_id)
        
        # Construct message with doctor's first name and last name
        doctor_name = f"{doctor.first_name} {doctor.last_name}"
        message_without_id = f"New Request Message From Doctor {doctor_name}"
        message_with_id = f"{message_without_id} (ID: {doctorrequest.id})"
        
        # Create DoctorSpecialistNotification without ID
        DoctorSpecialistNotification.objects.create(recipient=specialist, doctor_id=doctor_id, message=message_with_id)
        
        sender_email = "fetamasr@gmail.com"
        recipient_email = specialist.email
        try:
            send_email_with_retry(
                'New Message Notification',
                message_without_id,  # Send email without ID
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class DoctorPatientMessageViewSet(ModelViewSet):
    queryset = DoctorPatientMessage.objects.select_related('doctor','patient').all()
    serializer_class = DoctorPatientMessageSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctormessage = serializer.save()
        
        # Retrieve patient and doctor objects
        doctor_id = serializer.validated_data['doctor'].id
        patient_id = serializer.validated_data['patient'].id
        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        patient = User.objects.get(id=patient_id)
        
        # Construct message with doctor's first name and last name
        doctor_name = f"{doctor.first_name} {doctor.last_name}"
        message_without_id = f"New Message From Doctor {doctor_name}"
        message_with_id = f"{message_without_id} (ID: {doctormessage.id})"
        
        # Create DoctorPatientMessageNotification without ID
        DoctorPatientMessageNotification.objects.create(recipient=patient, doctor_id=doctor_id, message=message_with_id)
        
        sender_email = "fetamasr@gmail.com"
        recipient_email = patient.email
        try:
            send_email_with_retry(
                'New Message Notification From Doctor',
                message_without_id,  # Send email without ID
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class SpecialistDoctorResponseViewSet(ModelViewSet):
    queryset = SpecialistDoctorResponse.objects.select_related('specialist','doctor').all()
    serializer_class = SpecialistDoctorResponseSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        specialistresponse = serializer.save()
        doctor_id = serializer.validated_data['doctor'].id
        specialist_id = serializer.validated_data['specialist'].id
        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        specialist = User.objects.get(id=specialist_id)
        specialist_name = f"{specialist.first_name} {specialist.last_name}"
        
        # Construct the message without including the ID for email
        message_without_id = f"New Response Message From Specialist {specialist_name}"
        # Construct the full message including the ID for the database
        message_with_id = f"{message_without_id} (ID: {specialistresponse.id})"
        
        # Create SpecialistDoctorNotification without ID
        SpecialistDoctorNotification.objects.create(recipient=doctor, specialist_id=specialist_id, message=message_with_id)
        
        sender_email = "fetamasr@gmail.com"
        recipient_email = doctor.email
        print(doctor.email)
        try:
            send_email_with_retry(
                'New Message Notification From Specialist',
                message_without_id,  # Send email without ID
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    
class SpecialistDoctorRecommendationViewSet(ModelViewSet):
    queryset = SpecialistDoctorRecommendation.objects.select_related('specialist','doctor','patient')
    serializer_class=SpecialistDoctorRecommendationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        specialistrecommendation = serializer.save()
        doctor_id = serializer.validated_data['doctor'].id
        patient_id = serializer.validated_data['patient'].id
        specialist_id = serializer.validated_data['specialist'].id
        User = get_user_model()
        doctor = User.objects.get(id=doctor_id)
        patient = User.objects.get(id=patient_id)
        specialist = User.objects.get(id=specialist_id)
        specialist_name = f"{specialist.first_name} {specialist.last_name}"
        # Construct the message without including the ID for email
        message_without_id = f"New Recommendation Message From Specialist Name {specialist_name} for Patient {patient.first_name} {patient.last_name}"
        # Construct the full message including the ID for the database
        message_with_id = f"{message_without_id} (ID: {specialistrecommendation.id})"
        # Create SpecialistDoctorNotification without ID
        SpecialistDoctorNotification.objects.create(recipient=doctor, specialist_id=specialist_id, message=message_with_id)
        sender_email = "fetamasr@gmail.com"
        recipient_email = doctor.email
        print(doctor.email)
        try:
            send_email_with_retry(
                'New Message Notification From Specialist',
                message_without_id,  # Send email without ID
                sender_email,
                [recipient_email],
                retries=3,
                delay=5,
            )
        except Exception as e:
            logger.error(f"Failed to send email notification after multiple attempts: {e}")
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# class SegmentedImagePredictionTotalViewSet(ModelViewSet):
#     queryset = SegmentedImagePredictionTotal.objects.all()
#     serializer_class = SegmentedImagePredictionTotalSerializer
#     parser_classes = [MultiPartParser, FormParser]
#     def create(self, request):
#         serializer = SegmentedImagePredictionTotalSerializer(data=request.data)
#         if serializer.is_valid():
#             image = serializer.validated_data['image']
#             fss = FileSystemStorage()
#             filename = fss.save(image.name, image)
#             file_url = fss.url(filename)
#             file_path = os.path.join(settings.MEDIA_ROOT, filename)

#             try:
#                 # Load segmentation model
#                 segmentation_model_path = os.path.join(os.getcwd(), 'model_best_checkpoint.h5')
#                 with custom_object_scope({'bce_dice_loss': bce_dice_loss, 'iou_metric': iou_metric}):
#                     segmentation_model = load_model(segmentation_model_path)

#                 # Load classification model
#                 classification_model_path = os.path.join(os.getcwd(), 'modelres50.h5')
#                 classification_model = load_model(classification_model_path)

#                 # Segmentation
#                 input_image_seg = self.preprocess_image_segmentation(file_path)
#                 output_image = segmentation_model.predict(input_image_seg)
#                 output_path = os.path.join(settings.MEDIA_ROOT, 'segmentation_results', 'segmented_' + filename)
#                 self.save_output_image(output_image, output_path)

#                 # Classification
#                 classification_result = self.model_predict(file_path, classification_model)
#                 class_names = ['Glioma', 'Meningioma', 'Pituitary', 'No Tumour']
#                 predicted_class = class_names[classification_result[0]]

#                 # Save prediction to the database
#                 segmented_image_prediction = SegmentedImagePredictionTotal(
#                     image=image, segmentation_result=output_path, classification_result=predicted_class
#                 )
#                 segmented_image_prediction.save()

#                 # Return the response
#                 response_data = {
#                     'id': segmented_image_prediction.id,
#                     'segmentation_result_url': segmented_image_prediction.segmentation_result.url,
#                     'classification_result': predicted_class,
#                     'file_url': file_url
#                 }
#                 return Response(response_data, status=status.HTTP_200_OK)
            
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def preprocess_image_segmentation(self, image_path):
#         image = Image.open(image_path)
#         image = image.resize((128, 128))
#         image = image.convert('L')
#         input_image = np.array(image) / 255.0
#         input_image = input_image.reshape(1, 128, 128, 1)
#         return input_image

#     def preprocess_image_classification(self, image_path):
#         img = Image.open(image_path)
#         img = img.resize((200, 200))
#         img = img.convert('RGB')
#         img = np.array(img) / 255.0
#         img = np.expand_dims(img, axis=0)
#         return img

#     def model_predict(self, img_path, model):
#         img = self.preprocess_image_classification(img_path)
#         preds = model.predict(img)
#         pred = np.argmax(preds, axis=1)
#         return pred

#     def save_output_image(self, output_image, output_path):
#         output_image = np.squeeze(output_image)
#         output_image = (output_image * 255).astype(np.uint8)
#         if len(output_image.shape) == 2:
#             output_image = Image.fromarray(output_image, mode='L')
#         elif len(output_image.shape) == 3:
#             if output_image.shape[2] == 1:
#                 output_image = Image.fromarray(output_image[:, :, 0], mode='L')
#             elif output_image.shape[2] == 3:
#                 output_image = Image.fromarray(output_image, mode='RGB')
#             else:
#                 raise ValueError(f"Unexpected number of channels: {output_image.shape[2]}")
#         else:
#             raise ValueError(f"Unexpected array shape: {output_image.shape}")
#         os.makedirs(os.path.dirname(output_path), exist_ok=True)
#         output_image.save(output_path)





















class SegmentedImagePredictionTotalViewSet(ModelViewSet):
    queryset = SegmentedImagePredictionTotal.objects.all()
    serializer_class = SegmentedImagePredictionTotalSerializer
    parser_classes = [MultiPartParser, FormParser]
    def create(self, request):
        serializer = SegmentedImagePredictionTotalSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            fss = FileSystemStorage()
            filename = fss.save(image.name, image)
            file_url = fss.url(filename)
            file_path = os.path.join(settings.MEDIA_ROOT, filename)

            try:
                # Load segmentation model
                segmentation_model_path = os.path.join(os.getcwd(), 'model_best_checkpoint.h5')
                with custom_object_scope({'bce_dice_loss': bce_dice_loss, 'iou_metric': iou_metric}):
                    segmentation_model = load_model(segmentation_model_path)

                # Load classification model
                classification_model_path = os.path.join(os.getcwd(), 'modelres50.h5')
                classification_model = load_model(classification_model_path)

                # Segmentation
                input_image_seg = self.preprocess_image_segmentation(file_path)
                output_image = segmentation_model.predict(input_image_seg)
                output_path = os.path.join(settings.MEDIA_ROOT, 'segmentation_results', 'segmented_' + filename)
                self.save_output_image(output_image, output_path)
                # Classification
                classification_result = self.model_predict(file_path, classification_model)
                class_names = ['Glioma', 'Meningioma', 'Pituitary', 'No Tumour']
                predicted_class = class_names[classification_result[0]]

                # Save prediction to the database
                segmented_image_prediction = SegmentedImagePredictionTotal(
                    image=image, segmentation_result=output_path, classification_result=predicted_class
                )
                segmented_image_prediction.save()

                # Return the response
                response_data = {
                    'id': segmented_image_prediction.id,
                    'segmentation_result_url': segmented_image_prediction.segmentation_result.url,
                    'classification_result': predicted_class,
                    'file_url': file_url
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def preprocess_image_segmentation(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (128, 128))
        input_image = image / 255.0
        input_image = input_image.reshape(1, 128, 128, 1)
        return input_image

    def preprocess_image_classification(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (200, 200))
        img = img / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    def model_predict(self, img_path, model):
        img = self.preprocess_image_classification(img_path)
        preds = model.predict(img)
        pred = np.argmax(preds, axis=1)
        return pred

    def save_output_image(self, output_image, output_path):
        output_image = np.squeeze(output_image)
        output_image = (output_image * 255).astype(np.uint8)
        
        if len(output_image.shape) == 2:
            cv2.imwrite(output_path, output_image)
        elif len(output_image.shape) == 3:
            if output_image.shape[2] == 1:
                cv2.imwrite(output_path, output_image[:, :, 0])
            elif output_image.shape[2] == 3:
                cv2.imwrite(output_path, cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR))
            else:
                raise ValueError(f"Unexpected number of channels: {output_image.shape[2]}")
        else:
            raise ValueError(f"Unexpected array shape: {output_image.shape}")