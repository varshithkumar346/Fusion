from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from applications.globals.models import (HoldsDesignation,Designation)
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from applications.globals.models import User,ExtraInfo
from applications.complaint_system.models import Caretaker, StudentComplain, Supervisor, Workers
from . import serializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def complaint_details_api(request,detailcomp_id1):
    complaint_detail = StudentComplain.objects.get(id=detailcomp_id1)
    complaint_detail_serialized = serializers.StudentComplainSerializers(instance=complaint_detail).data
    if complaint_detail.worker_id is None:
        worker_detail_serialized = {}
    else :
        worker_detail = worker_detail.objects.get(id=complaint_detail.worker_id)
        worker_detail_serialized = serializers.WorkersSerializers(instance=worker_detail).data
    complainer = User.objects.get(username=complaint_detail.complainer.user.username)
    complainer_serialized = serializers.UserSerializers(instance=complainer).data
    complainer_extra_info = ExtraInfo.objects.get(user = complainer)
    complainer_extra_info_serialized = serializers.ExtraInfoSerializers(instance=complainer_extra_info).data
    response = {
        'complainer' : complainer_serialized,
        'complainer_extra_info':complainer_extra_info_serialized,
        'complaint_details' : complaint_detail_serialized,
        'worker_details' : worker_detail_serialized
    }
    return Response(data=response,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def student_complain_api(request):
    user = get_object_or_404(User,username = request.user.username)
    user = ExtraInfo.objects.all().filter(user = user).first()
    if user.user_type == 'student':
        complain = StudentComplain.objects.filter(complainer = user)
    elif user.user_type == 'staff':
        staff = ExtraInfo.objects.get(id=user.id)
        staff = Caretaker.objects.get(staff_id=staff)
        complain = StudentComplain.objects.filter(location = staff.area)
    elif user.user_type == 'faculty':
        faculty = ExtraInfo.objects.get(id=user.id)
        faculty = Supervisor.objects.get(sup_id=faculty)
        complain = StudentComplain.objects.filter(location = faculty.area)
    complains = serializers.StudentComplainSerializers(complain,many=True).data
    resp = {
        'student_complain' : complains,
    }
    return Response(data=resp,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def worker_api(request):
    worker = Workers.objects.all()
    workers = serializers.WorkersSerializers(worker,many=True).data

    resp = {
        'workers' : workers,
    }
    return Response(data=resp,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def caretaker_api(request):
    caretaker = Caretaker.objects.all()
    caretakers = serializers.CaretakerSerializers(caretaker,many=True).data
    resp = {
        'waretakers' : caretakers,
    }
    return Response(data=resp,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def supervisor_api(request):
    supervisor = Supervisor.objects.all()
    supervisors = serializers.SupervisorSerializers(supervisor,many=True).data

    resp = {
        'supervisors' : supervisors,
    }
    return Response(data=resp,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_complain_api(request):
    serializer = serializers.StudentComplainSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def add_worker_api(request):
    serializer = serializers.WorkersSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def remove_worker_api(request,w_id):
    if Workers.objects.filter(id=w_id).exists():
        worker = Workers.objects.get(id = w_id)
        worker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else :
        return Response(status=status.HTTP_404_NOT_FOUND)