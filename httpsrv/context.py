from django.conf import settings 
from .models import * 

def check_user_has_active_questions(request ): 
    # Get questions with remaining=0 for this user 
    user_active_questions = Question_Profile.objects.filter(
            remaining=0, 
            profile=request.user.profile
        )
    # even if remaining is 0 for one of the relationships, verify that the user
    # is CURRENTLY JOINED/SUBSCRIBED TO THAT QUESTION'S COURSE; if they are not, 
    # do not say they have active questions 
    has_active_questions = False
    for q in user_active_questions: 
        if CourseSubscription.objects.filter(
            profile=request.user.profile,
            course_id=q.question.course_set.all()[0].id):
            # User subscribed to this question's course, mark as active 
            has_active_questions = True 
            break 
    return has_active_questions, user_active_questions

    

def context(request):
    """ Custom context processor; define context available to all templates """
    # Always return the AWS API Endpoints to front end for direct use by Javascript
    context = {
        'RENDER_QUESTION_ENDPOINT': settings.RENDER_QUESTION_ENDPOINT,
        'CREATE_QUESTION_ENDPOINT': settings.CREATE_QUESTION_ENDPOINT,
        'GET_ANSWER_ENDPOINT': settings.GET_ANSWER_ENDPOINT,
        'CHECK_ANSWER_ENDPOINT': settings.CHECK_ANSWER_ENDPOINT,
    }
    context['base_unit'] = settings.BASE_UNIT
    if request.user.is_authenticated:
        context['AKREAD'] = request.user.profile.read_api_key
        context['AKCUD'] = request.user.profile.cud_api_key 
        # Get the courses this authenticated user is subscribed to 
        context['subscribed_courses'] = Course.objects.filter(id__in=list(
                CourseSubscription.objects.filter(
                    profile=request.user.profile).values_list('course_id',flat=True)))
        context['student'] = request.user.profile.account_type == 'student'
        context['instructor'] = request.user.profile.account_type == 'instructor'  

        user_has_active_questions, active_questions_for_user = check_user_has_active_questions(request)
        context['has_active_questions'] = user_has_active_questions
        # determine which of the courses this user is subscribed to has the active questions
        active_qids = list(active_questions_for_user.values_list('question_id', flat=True))
        for qid in active_qids:  
            for sc in context['subscribed_courses']: 
                # if this active question belongs to this course, mark course as active 
                if sc.questions.filter(id=qid).exists(): 
                    setattr(
                        sc,
                        'active',
                        True
                    )
            
            
    return context 