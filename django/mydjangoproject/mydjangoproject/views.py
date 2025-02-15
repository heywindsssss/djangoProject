from django.http import HttpResponse




from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .model import EvaluationRequest
import json


@csrf_exempt  # Only for testing; use proper authentication in production
def submit_evaluation_request(request):
   if request.method == "POST":
       try:
           data = json.loads(request.body)  # Parse JSON data
           input_prompt = data.get("input_prompt")  # Get input_prompt from request


           if not input_prompt:
               return JsonResponse({"error": "Input prompt is required"}, status=400)


           # Create evaluation request
           evaluation = EvaluationRequest.objects.create(input_prompt=input_prompt)


           return JsonResponse({
               "id": str(evaluation.id),
               "input_prompt": evaluation.input_prompt,
               "status": evaluation.status,
               "result": evaluation.result,
               "created_at": evaluation.created_at.isoformat(),
               "updated_at": evaluation.updated_at.isoformat()
           }, status=201)


       except json.JSONDecodeError:
           return JsonResponse({"error": "Invalid JSON format"}, status=400)


   return JsonResponse({"error": "Invalid request method"}, status=405)
def get_evaluation_result(request, request_id):
   evaluation = get_object_or_404(EvaluationRequest, id=request_id)
  
   return JsonResponse({
       'id': str(evaluation.id),
        'status': evaluation.status,
       'result': evaluation.result,
       'created_at': evaluation.created_at.isoformat(),
       'updated_at': evaluation.updated_at.isoformat(),
   })

