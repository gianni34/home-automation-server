from django.contrib import admin
from HomeAutomation.forms import *
from HomeAutomation.models import *

admin.site.register(ArtifactCode)
admin.site.register(VariableType)
admin.site.register(SceneAction)
admin.site.register(VariableRange)
admin.site.register(SSHConfig)
admin.site.register(WSConfig)
admin.site.register(Zone)
admin.site.register(ArtifactType)
admin.site.register(StateVariable)
admin.site.register(Scene)


class VariableRangeInLine(admin.StackedInline):
    model = VariableRange
    extra = 0


class StateVariableInLine(admin.StackedInline):
    model = StateVariable
    inlines = [VariableRangeInLine]
    extra = 0


class ArtifactAdmin(admin.ModelAdmin):
    inlines = [StateVariableInLine]
    extra = 0


class IntermediaryAdmin(admin.ModelAdmin):
    form = IntermediaryForm


class UserAdmin(admin.ModelAdmin):
    form = UserForm


admin.site.register(Intermediary, IntermediaryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Artifact, ArtifactAdmin)
