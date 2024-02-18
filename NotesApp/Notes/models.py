# models.py
from django.contrib.auth.models import User
from django.db import models
# import uuid

class Note(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class NoteHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title