from django.contrib import admin
from questions.models import QuestionCapture, ZoneImage, QuestionChoixMultiple, Choix

class ZoneImageInline(admin.TabularInline):
    model = ZoneImage
    extra = 1

class QuestionCaptureAdmin(admin.ModelAdmin):
    fields = ['question', 'image']
    inlines = [ZoneImageInline,]
    
    class Media:
        css = {
            "all": ("css/styles.css",)
            }
        js = ("js/jquery-1.9.0.min.js","js/script.js")

class ChoixInline(admin.TabularInline):
    model = Choix
    extra = 1

class QuestionChoixMultipleAdmin(admin.ModelAdmin):
    inlines = [ChoixInline,]

admin.site.register(QuestionCapture, QuestionCaptureAdmin)
admin.site.register(QuestionChoixMultiple, QuestionChoixMultipleAdmin)