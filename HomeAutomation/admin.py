from django.contrib import admin
from HomeAutomation.models import *

admin.site.register(SSHConfig)
admin.site.register(WSConfig)
admin.site.register(Parameters)
admin.site.register(Zone)
admin.site.register(Intermediary)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(ArtifactType)
admin.site.register(StateVariable)
admin.site.register(Scene)


class StateVariableInLine(admin.StackedInline):
    model = StateVariable
    extra = 0


class ArtifactAdmin(admin.ModelAdmin):
    inlines = [StateVariableInLine]
    extra = 0


admin.site.register(Artifact, ArtifactAdmin)



