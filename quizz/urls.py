from django.conf.urls import patterns, include, url
from django.conf import settings
from questions.models import QuestionCapture
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/accounts/login/?next=/test/'}),

    # testing
    url(r'^test/(?P<exam_id>\d+)/$', 'examens.views.exam_for_user'),
    url(r'^test/(?P<exam_id>\d+)/(?P<question_id>\d+)/answer/$', 'examens.views.answer_exam_question'),
    url(r'^test/$', 'examens.views.exams_for_user'),
    
)
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)
