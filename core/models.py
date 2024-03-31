from django.db import models

# Create your models here.
class Session(models.Model):
  session_key = models.CharField(max_length=40, primary_key=True)
  current_question_id = models.IntegerField(blank=True, null=True)
  message_history = models.JSONField(default=list)

  def __str__(self):
    return f"Session: {self.session_key}"
