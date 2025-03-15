from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from app.user_service import UserService
from app.common_exceptions import ValidationError, InternalServerError
from app.user_exceptions import EmailAlreadyExistsException


# Create your views here.
@csrf_exempt
def register_user(request: HttpRequest) -> JsonResponse:
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        try:
            response = UserService.add_user(data)
            return JsonResponse(response, status=201)
        except ValidationError as ex:
            return JsonResponse({"error": str(ex)}, status=400)
        except EmailAlreadyExistsException as ex:
            return JsonResponse({"error": str(ex)}, status=409)
        except InternalServerError as ex:
            return JsonResponse({"error": str(ex)}, status=500)
    return JsonResponse(
        {"error": f"** {request.method} is not allowed. **"}, status=405
    )


@csrf_exempt
def get_user_profiles(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        try:
            response = UserService.get_users()
            return JsonResponse(response, status=200)
        except InternalServerError as ex:
            return JsonResponse({"error": str(ex)}, status=500)
    return JsonResponse(
        {"error": f"** {request.method} is not allowed. **"}, status=405
    )
