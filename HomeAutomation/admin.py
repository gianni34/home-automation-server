from django.contrib import admin
from HomeAutomation.models import ArtifactType, Intermediary, Artifact, Zone, Role, User, State
# Register your models here.

admin.site.register(Zone)
admin.site.register(Intermediary)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(ArtifactType)
admin.site.register(State)
admin.site.register(Artifact)
