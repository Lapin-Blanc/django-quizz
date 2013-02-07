from django.shortcuts import render, get_object_or_404
from questions.models import QuestionCapture
from django.http import HttpResponse

def render_question(request, question_id):
    q = get_object_or_404(QuestionCapture, id=question_id)
    return render(request, "questions/question.html", {"question":q})

def answer_question(request, question_id):
    q = get_object_or_404(QuestionCapture, id=question_id)
    x = request.POST.get("x",None)
    y = request.POST.get("y",None)
    if x and y:
        result = q.check_answer(int(x), int(y))
        if result:
            return HttpResponse('<h2 style="color:forestgreen;">Bien !</h2><a href="/">Autre question</a>')
    return HttpResponse('<h2 style="color:firebrick;">Pas bien !</h2><a href="/">Autre question</a>')