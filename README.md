# MyDjangoProject

## Overview
MyDjangoProject is a Django-based web application that utilizes Celery for background task processing and Redis as a message broker. It includes an email notification system using Resend API to notify users when an evaluation request is completed.

## Features
- **Task Queueing with Celery**: Asynchronous task processing using Celery.
- **Redis as a Message Broker**: Redis is used to manage task queues.
- **Email Notifications**: Uses Resend API to send email notifications upon task completion.
- **Django Backend**: Handles API requests and task execution.
- **Docker Support (Optional)**: Easily deployable with Docker and Docker Compose.

## Project Design

### Architecture
The project follows a modular architecture:
- **Django App**: Handles API requests and database operations.
- **Celery Worker**: Runs background tasks asynchronously.
- **Redis**: Acts as a message broker for Celery.
- **Resend API**: Sends email notifications.

### Flow Diagram
1. User submits an evaluation request via API.
2. Django saves the request and triggers a Celery task.
3. Celery processes the evaluation asynchronously.
4. Upon completion, Celery triggers an email notification using Resend API.
5. The user receives an email with the evaluation results.

## Implementation

### 1. Setup Celery in Django
- Install Celery and Redis:
  ```sh
  pip install celery redis
  ```
- Configure Celery in `settings.py`:
  ```python
  CELERY_BROKER_URL = 'redis://localhost:6379/0'
  CELERY_ACCEPT_CONTENT = ['json']
  CELERY_TASK_SERIALIZER = 'json'
  ```
- Create `celery.py` in your Django project:
  ```python
  from __future__ import absolute_import, unicode_literals
  import os
  from celery import Celery
  
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mydjangoproject.settings')
  
  app = Celery('mydjangoproject')
  app.config_from_object('django.conf:settings', namespace='CELERY')
  app.autodiscover_tasks()
  ```

### 2. Define Celery Task
Create a `tasks.py` file inside your Django app:
```python
from celery import shared_task
from resend import Emails

@shared_task
def process_evaluation(request_id, evaluation_result):
    """Processes evaluation and sends email notification."""
    params = Emails.SendParams(
        from_="srivastava.windhya@gmail.com",
        to=["windhya.srivastava@gmail.com"],
        subject="Evaluation Complete",
        html=f"<strong>Your evaluation request (ID: {request_id}) is complete.</strong><br>Result: {evaluation_result}",
    )
    Emails.send(params)
```

### 3. Run Celery Worker
Start the Celery worker:
```sh
celery -A mydjangoproject worker --loglevel=info
```

### 4. API Endpoint to Trigger Task
Add an API endpoint in `views.py`:
```python
from django.http import JsonResponse
from .tasks import process_evaluation

def evaluate(request):
    request_id = "12345"
    evaluation_result = "Passed"
    process_evaluation.delay(request_id, evaluation_result)
    return JsonResponse({"message": "Evaluation request received."})
```

## Running the Project
1. Start Redis Server:
   ```sh
   redis-server
   ```
2. Start Django Server:
   ```sh
   python manage.py runserver
   ```
3. Start Celery Worker:
   ```sh
   celery -A mydjangoproject worker --loglevel=info
   ```
4. Send an API request to trigger an evaluation.

## Conclusion
This project efficiently processes evaluation requests asynchronously using Celery and Redis. It also integrates an automated email notification system using the Resend API.

## Future Enhancements
- Add a front-end UI for request submission.
- Implement authentication for API access.
- Store evaluation results in a database.
- Improve error handling and logging.

---
Feel free to contribute or raise issues! 🚀



---

## 👩‍💻 Author
**Windhya Srivastava**  
🔗 [GitHub](https://github.com/heywindsssss) | 📧 srivastava.windhya@gmail.com

