from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user=models.ForeignKey(
        User, 
        on_delete=models.CASCADE, default = None)
    name=models.CharField(max_length=100)
    isDone=models.BooleanField(default=False)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.name