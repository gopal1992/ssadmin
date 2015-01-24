from django.db import models

class HealthCheck(models.Model):
    test_key = models.CharField(max_length=255)

    def __unicode__(self):
        return self.test_key