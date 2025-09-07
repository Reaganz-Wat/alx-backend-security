from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
@ratelimit(key='ip', rate='10/m', method='POST', block=True, condition=lambda r: r.user.is_authenticated)
@ratelimit(key='ip', rate='5/m', method='POST', block=True, condition=lambda r: not r.user.is_authenticated)
def login_view(request):
    if request.method == "POST":
        # fake login logic (just return success for demo)
        return JsonResponse({"message": "Login attempted", "user": str(request.user)})
    return JsonResponse({"error": "Only POST allowed"}, status=405)