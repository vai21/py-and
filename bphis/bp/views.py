from django.shortcuts import render
from django.http import HttpResponse
from .serializers import BpSerializer
from .models import Bp
from rest_framework import permissions, viewsets

# Create your views here.
def index(request):
  return HttpResponse("BP Module")

class BpViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bp to be viewed or edited.
    """
    queryset = Bp.objects.all().order_by('-created_at')
    serializer_class = BpSerializer
    # permission_classes = [permissions.IsAuthenticated]

