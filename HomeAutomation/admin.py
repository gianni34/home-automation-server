from django.contrib import admin
#from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline
from HomeAutomation.models import *

admin.site.register(Parameters)
admin.site.register(Zone)
admin.site.register(Intermediary)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(ArtifactType)
admin.site.register(StateVariable)


class StateVariableInLine(admin.StackedInline):
    model = StateVariable
    extra = 0


class ArtifactAdmin(admin.ModelAdmin):
    inlines = [StateVariableInLine]
    extra = 0


admin.site.register(Artifact, ArtifactAdmin)



