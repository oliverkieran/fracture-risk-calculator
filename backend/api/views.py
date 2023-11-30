from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer


@api_view(["POST"])
def getRisk(request):
    serializer = PatientSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        print("Data:", data)
        data["bmi"] = round(data["weight"] / ((data["height"] / 100) ** 2), 2)

        # serializer.save()
        return Response({"message": "Risk score successfully calculated.", "risk": 0.5})
    else:
        print("Errors:", serializer.errors)
        return Response(serializer.errors)
