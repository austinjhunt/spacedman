from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .views import * 
 
urlpatterns = [
    path('create_question/', login_required(CreateQuestionView.as_view()), name='create_question'), 
    path('create_course/', login_required(CreateCourseView.as_view()), name='create_course'),
    path('edit_course/<slug:course_id>/', login_required(EditCourseView.as_view()), name='edit_course'),
    path('questions', staff_member_required(QuestionListView.as_view()), name='questions'),
    path('courses', CourseListView.as_view(), name='courses'),
    path('subscribe/<slug:course_id>', login_required(SubscribeView.as_view()), name='subscribe'),
    path('practice/<slug:course_id>', login_required(PracticeView.as_view()), name='practice'), 
    path('render-question/<slug:qid>/<int:instances>', login_required(RenderQuestionView.as_view()), name='render-question'),
    path('check-answer/', login_required(CheckAnswerView.as_view()), name='check-answer'),
    # Account management 
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')), 

    path('testaws', TestAWS.as_view(),name='test-aws'),

    path('', HomeView.as_view()),
]