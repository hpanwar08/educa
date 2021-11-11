from django.conf import settings
from django.db import models


class Message(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    group_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_json(self):
        return {
            'message_id': self.id,
            'creator': self.creator.email,
            'content': self.content,
            'group_name': self.group_name,
            'created_at': self.created_at.isoformat()
        }

    def __str__(self):
        return f"{self.creator}"

    class Meta:
        ordering = ('-created_at',)
