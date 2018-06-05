from django.contrib import admin
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline
from HomeAutomation.models import *

admin.site.register(Zone)
admin.site.register(Intermediary)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(ArtifactType)
admin.site.register(ValueVariable)
admin.site.register(RangeVariable)
admin.site.register(BooleanVariable)


#@admin.register(ValueVariable)
class ValueVariableInLine(admin.StackedInline):
    model = ValueVariable
    extra = 0


#@admin.register(BooleanVariable)
class BooleanVariableInLine(admin.StackedInline):
    model = BooleanVariable
    extra = 0


#@admin.register(RangeVariable)
class RangeVariableInLine(admin.StackedInline):
    model = RangeVariable
    extra = 0

#@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    inlines = [ValueVariableInLine, RangeVariableInLine, BooleanVariableInLine]
    extra = 0


admin.site.register(Artifact, ArtifactAdmin)



