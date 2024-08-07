# webapp/utils/models.py
import uuid
from django.db import models

# models.py
class CommonFields(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    status = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True, editable=False)
    updated_by = models.CharField(max_length=40, null=True, blank=True, editable=False)

    class Meta:
        abstract = True



