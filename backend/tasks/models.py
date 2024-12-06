from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='tasks/audio/')
    transcription = models.TextField(blank=True, null=True)
    calendar_event_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

