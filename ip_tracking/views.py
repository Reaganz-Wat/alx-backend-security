from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse

# Create your views here.
def try_caching(request):
    user = cache.get("user:1")
    return JsonResponse({"user": user})