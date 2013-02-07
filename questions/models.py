# -*- coding: utf-8 -*-

# TODO categorize questions...

from django.db import models
from django.template import loader, Context
from django.http import HttpResponse

# Classe Question principale
class Question(models.Model):
    question = models.TextField(default="Entrez le texte de la question ici...", help_text="Les balises HTML sont accept&eacute;es")
    
    def __unicode__(self):
        type = getattr(self._get_subclass_question(),"type","")
        return type + ": " + self.question
    
    def _get_questiontype(self):
        from django.db.models.fields.related import SingleRelatedObjectDescriptor
        subclass_question_types = [a for a in dir(Question) if isinstance(getattr(Question, a), SingleRelatedObjectDescriptor)]
        for subclass_question_type in subclass_question_types:
            if hasattr(self, subclass_question_type):
                return subclass_question_type

    def _get_subclass_question(self):
        return getattr(self, self._get_questiontype())
    
    def check_answer(self, *args, **kwargs):
        return self._get_subclass_question().check_answer(*args, **kwargs)

    def render_to_html(self, q_position, answer_url):
        q = self._get_subclass_question()
        t = loader.get_template(q.template)
        return t.render(Context({"question":q,"q_position":q_position,"answer_url":answer_url}))
    
        
class QuestionCapture(Question):
    # Class attributes
    type = "Capture"
    template = "questions/question_capture.html"

    # Capture specific attributes
    image = models.ImageField(upload_to="captures")
    
    def check_answer(self, x, y):
        x = int(x[0])
        y = int(y[0])
        for z in self.zoneimage_set.all():
            if x>=z.x and x<=z.x+z.width and y>=z.y and y<=z.y+z.height:
                return True
        return False

    # TODO improve and decouple from urls
    def get_absolute_url(self):
        return "/questions/captures/%s/" % self.id

class ZoneImage(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    question = models.ForeignKey(QuestionCapture)
    
    def __unicode__(self):
        return str((self.x, self.y, self.width, self.height))

class QuestionChoixMultiple(Question):
    type = "QCM"
    template = "questions/question_choix_multiple.html"

    def check_answer(self, answer):
        return self.choix_set.get(id=int(answer[0])).correct
        
    # TODO improve, factorize /questions/ and add for staff only
    def get_absolute_url(self):
        return "/questions/choixmultiple/%s/" % self.id
        
class Choix(models.Model):
    choix = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(QuestionChoixMultiple)
    
    def __unicode__(self):
        return self.choix

