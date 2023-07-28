from django.db import models

from accounts.models import User

from ..read_aloud.models import ReadAloud


class Discussion(models.Model):
    read_aloud = models.ForeignKey(ReadAloud, blank=True, null=True, on_delete=models.CASCADE)
    # answer = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="discussion")
    body = models.TextField()
    like = models.ManyToManyField(User, related_name="like", blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_like(self):
        return self.like.count()

    def total_replies(self):
        return Discussion.objects.filter(parent=self.id).count()

    def __str__(self):
        return self.body if len(self.body) < 25 else self.body[:24]+"..."

