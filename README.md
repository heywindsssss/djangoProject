# Django Celery Email Processing

This project demonstrates how to use **Celery** with **Django** to process background tasks such as sending emails using **Resend API**.

## 🚀 Features
- **Django Backend**: Handles requests and manages email processing.
- **Celery Worker**: Asynchronous task execution.
- **Redis as Message Broker**: For task queuing.
- **Resend API Integration**: Email delivery service.

---

## 📌 Setup & Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/yourusername/your-repository.git
cd your-repository
```

### 2️⃣ Create & Activate Virtual Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure `.env`
Create a `.env` file in the project root and add:
```ini
RESEND_API_KEY=your_resend_api_key
REDIS_URL=redis://localhost:6379/0
DJANGO_SECRET_KEY=your_secret_key
```

### 5️⃣ Run Redis Server (if not already running)
```sh
redis-server
```

### 6️⃣ Run Migrations & Start Django Server
```sh
python manage.py migrate
python manage.py runserver
```

### 7️⃣ Start Celery Worker
```sh
celery -A mydjangoproject worker --loglevel=info
```

---

## 📨 Sending Emails with Celery & Resend
Inside your Django views or tasks:
```python
import resend
from mydjangoproject.celery import app

resend.api_key = "your_resend_api_key"

@app.task
def send_email_task(to_email, request_id, evaluation_result):
    params = resend.Emails.SendParams(
        from_="Windhya <srivastava.windhya@gmail.com>",
        to=[to_email],
        subject="Evaluation Complete",
        html=f"""
            <strong>Your evaluation request (ID: {request_id}) is complete.</strong><br>
            Result: {evaluation_result}
        """,
    )
    resend.Emails.send(params)
```

Trigger the email task in your Django view:
```python
from myapp.tasks import send_email_task

def evaluation_complete(request):
    send_email_task.delay("windhya.srivastava@gmail.com", "12345", "Success")
    return JsonResponse({"message": "Email task triggered!"})
```

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 👩‍💻 Author
**Windhya Srivastava**  
🔗 [GitHub](https://github.com/yourusername) | 📧 windhya.srivastava@gmail.com

