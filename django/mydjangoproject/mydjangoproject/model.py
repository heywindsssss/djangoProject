from django.db import models
import uuid


class EvaluationRequest(models.Model):
   STATUS_CHOICES = [
       ('pending', 'Pending'),
       ('completed', 'Completed'),
   ]


   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
   input_prompt = models.TextField()
   status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
   result = models.TextField(blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)


   def __str__(self):
       return f"Request {self.id} - {self.status}"