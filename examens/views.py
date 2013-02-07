# -*- coding:utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from examens.models import Examen, ExamenLine
from django.utils import timezone

@login_required
def exams_for_user(request):
    utilisateur = request.user
    return render(request, "examens/liste_examens.html", {"exams_list":request.user.examen_set.all()})

@login_required
def exam_for_user(request, exam_id):
    exam = get_object_or_404(Examen, id=exam_id, utilisateur=request.user)
    if not exam.debut:
        exam.debut = timezone.now()
    exam.save()
    unanswered_questions = exam.examenline_set.filter(repondu=None)
    if unanswered_questions:
        next_question = unanswered_questions[0]
        q_questionnaire = next_question.question_line
        q_position = q_questionnaire.position
        return render(request, "examens/examen.html", { "exam":exam, 
                                                        "elapsed":(timezone.now()-exam.debut).seconds,
                                                        "total":exam.questionnaire.duree * 60,
                                                        "question_html":q_questionnaire.question.render_to_html(q_position=q_position, answer_url="/test/%s/%s/answer/" % (exam_id, next_question.id)),
                                                        })
    else:
        #Examen terminé ou bien sans questions à gérer
        from django.db.models import Sum
        if not exam.fin:
            exam.fin = timezone.now()
        exam.resultat = exam.examenline_set.aggregate(Sum('resultat'))['resultat__sum']
        total = exam.questionnaire.questionline_set.aggregate(Sum('ponderation'))['ponderation__sum']
        exam.save()
        return HttpResponse("""
        <h1>Test terminé</h1>
        <h2>R&eacute;sultat:&nbsp;%0d/%s</h2>
        <a href="/test/">Retour aux tests...</a>
        """ % (round(exam.resultat,0),total))

@login_required
def answer_exam_question(request, exam_id, question_id):
    exam_question = get_object_or_404(ExamenLine, id=question_id, examen=exam_id, examen__utilisateur=request.user)
    answer = dict(request.POST)
    answer.pop('csrfmiddlewaretoken')
    exam_question.repondu = exam_question.question_line.question.check_answer(**answer)
    exam_question.save()
    return HttpResponseRedirect('/test/%s/' % exam_id)

