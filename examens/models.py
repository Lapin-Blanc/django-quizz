# -*- coding: utf-8 -*-
from django.db import models
from questions.models import Question
from django.contrib.auth.models import User

class Questionnaire(models.Model):
    nom = models.CharField(max_length=20,help_text="Nom descriptif du questionnaire")
    duree = models.IntegerField("Durée",help_text="Exprimée en minutes")
    
    def __unicode__(self):
        return self.nom

class QuestionLine(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    position = models.IntegerField()
    question = models.ForeignKey(Question)
    ponderation = models.IntegerField("Pondération", default=1)
    
    def __unicode__(self):
        return u"%s - %s" % (self.position, self.question)
    
    class Meta:
        ordering = ['position',]

class Examen(models.Model):
    utilisateur = models.ForeignKey(User)
    questionnaire = models.ForeignKey(Questionnaire)
    debut = models.DateTimeField("Début du test", null=True, blank=True)
    fin = models.DateTimeField("Fin du test", null=True, blank=True)
    resultat = models.DecimalField("Résultat", max_digits=4, decimal_places=1, null=True, blank=True)
    
    def __unicode__(self):
        return u"%s - %s" % (self.utilisateur, self.questionnaire)
    
    def get_absolute_url(self):
        return "/test/%s/" % self.id
    
    def save(self, *args, **kwargs):
        super(Examen, self).save(*args, **kwargs)
        if not self.examenline_set.all():
            for q in self.questionnaire.questionline_set.all():
                self.examenline_set.create(question_line=q)

class ExamenLine(models.Model):
    examen = models.ForeignKey(Examen)
    question_line = models.ForeignKey(QuestionLine)
    repondu = models.NullBooleanField("Correct", null=True, blank=True)
    resultat = models.DecimalField("Résultat", max_digits=4, decimal_places=1, null=True, blank=True)
    
    def __unicode__(self):
        return self.question_line.__unicode__()
    
    def save(self, *args, **kwargs):
        if not self.repondu==None:
            if self.repondu:
                self.resultat = self.question_line.ponderation
            else:
                self.resultat = 0
        super(ExamenLine, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['question_line__position',]
