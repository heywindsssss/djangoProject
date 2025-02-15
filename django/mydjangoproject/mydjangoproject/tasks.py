import time
import os
import resend
from celery import shared_task
from .model import EvaluationRequest

# Set Resend API key from environment variable
resend.api_key = os.environ.get("RESEND_API_KEY")

@shared_task
def process_evaluation(request_id):
    """Simulates evaluation and sends an email via Resend."""
    time.sleep(5)  # Simulate evaluation delay

    try:
        evaluation = EvaluationRequest.objects.get(id=request_id)
        evaluation.result = f"Generated response for: {evaluation.input_prompt}"
        evaluation.status = "completed"
        evaluation.save()

        # Send email notification via Resend API
        params = resend.Emails.SendParams(
            from_="Windhya <srivastava.windhya@gmail.com>",  
            to=["windhya.srivastava@gmail.com"],  # Recipient email
            subject="Evaluation Complete",
            html=f"<strong>Your evaluation request (ID: {request_id}) is complete.</strong><br>Result: {evaluation.result}",
        )
        resend.Emails.send(params)


    except EvaluationRequest.DoesNotExist:
        print(f"Error: Evaluation request with ID {request_id} not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")
