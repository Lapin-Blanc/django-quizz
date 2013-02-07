from django.contrib import admin
from examens.models import Questionnaire, QuestionLine, Examen, ExamenLine

class QuestionLineInline(admin.TabularInline):
    model = QuestionLine
    extra = 1

class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionLineInline,]
    
class ExamenLineInline(admin.TabularInline):
    model = ExamenLine
    extra = 0
    
class ExamenAdmin(admin.ModelAdmin):
    inlines = [ExamenLineInline,]

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Examen, ExamenAdmin)
