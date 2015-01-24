from django.contrib import admin

from health_check.models import HealthCheck


admin.site.register(HealthCheck)
