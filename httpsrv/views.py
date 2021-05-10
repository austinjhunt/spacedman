import os, re, random
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.http import JsonResponse
from django.views.generic import View, TemplateView, ListView, FormView, CreateView 
from .forms import * 
from django.conf import settings 
BASE_UNIT = settings.BASE_UNIT
aws_lambda_api_url = os.environ.get('AWS_LAMBDA_API_GATEWAY_URL','')
# Create your views here.

class HomeView(View): 
    def get(self, request): 
        return render(
            request, 
            template_name="index.html",
            context={}
        )

class TestAWS(TemplateView):
    template_name = 'test.html'

class CreateQuestionView(FormView):
    template_name = 'create_question.html'
    form_class = CreateQuestionForm
    def get(self, request):         
        return render(
            request, 
            template_name=self.template_name,
            context={
                'form': self.form_class
            }
        ) 

class QuestionListView(ListView): 
    template_name = 'questions.html'
    model = Question 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subjects = list(self.model.objects.all().values_list('subject_area',flat=True).distinct())
        print(subjects)
        sdict = {}
        for s in subjects: 
            sdict[s] = Question.objects.filter(subject_area=s)
        context['subjects'] = sdict
        return context 

class CourseListView(ListView):
    model = Course 
    template_name = 'courses.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['all_courses'] = Course.objects.all()
        if self.request.user.is_authenticated:
            # indicate which courses belong to requesting user  
            for c in context['all_courses']: 
                setattr(
                    c, 'user_subscribed', 
                    CourseSubscription.objects.filter(
                        profile=self.request.user.profile,
                        course=c).exists()
                ) 
                print(c.instructor.user.first_name)
        print(context)
        return context  

class EditCourseView(View): 
    def get(self, request, course_id): 
        course = None
        if Course.objects.filter(id=course_id).exists():
            course = Course.objects.get(id=course_id)
        context = {
            'title': 'Edit Course',
            'create_question_form': CreateQuestionForm(),
            'course': course
        } 
        return render(
            request, 
            template_name='create_course.html', 
            context=context
        )
    def post(self, request, course_id): 
        course = Course.objects.get(id=course_id)
        # only allow if requestor owns course 
        if course.instructor.user == request.user: 
            print('allowed to edit')
            # create and add questions to course 
            new_question_indices = []
            for key, val in request.POST.items(): 
                if "hidden-question-index" in key: 
                    # # new question 
                    # # get the index 
                    # index = val 
                    # new_question = Question(
                        
                    # )  
                    new_question_indices.append(val) 
            for i in new_question_indices: 
                # new question for each index 
                prefix = f"question-{i}-" # prefix for fields of this question
                new_question = Question(
                    question_template=request.POST.get(f"{prefix}question-template", None),
                    answer_template=request.POST.get(f"{prefix}answer-template", None),
                    code=request.POST.get(f"{prefix}code", None),
                    code_context=request.POST.get(f"{prefix}code-context", None),
                    subject_area=request.POST.get(f"{prefix}subject-area", "").lower()
                )
                if new_question.validate_fields(): 
                    new_question.save()
                course.questions.add(new_question)
            course.save()
            return redirect('/courses')
        else: 
            return JsonResponse(
                {'error': f"You are not allowed to edit the course: {course.course_title}"}
                )

class CreateCourseView(View):   
    template_name = 'create_course.html'
    def get(self, request): 
        context = {}
        context['title'] = 'Create Course' 
        context['create_question_form'] = CreateQuestionForm()
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request): 
        # get the course title first  
        course_title = request.POST.get('course-title', None) 
        # Create a course 
        course = Course(
            instructor=request.user.profile,
            course_title=course_title
        )
        course.save()  
        return redirect(f'/edit_course/{course.id}')
 
class SubscribeView(View): 
    """ View for subscribing to course; assume authenticated """
    def get(self, request, course_id):
        course_title = Course.objects.get(id=course_id).course_title
        operation = int(request.GET.get('op'))
        if operation == 1: 
            # subscribe
            print('subscribe')
            if CourseSubscription.objects.filter(
                profile=request.user.profile,
                course_id=course_id
            ).count() == 0:
                CourseSubscription(
                    profile=request.user.profile,
                    course_id=course_id
                    ).save()
                # you need to create a new question_profile object for each question in 
                # this course if it's not already created 
                course = Course.objects.get(id=course_id)
                for q in course.questions.all(): 
                    if Question_Profile.objects.filter(
                        profile=request.user.profile,
                        question=q
                    ).count() == 0: 
                        Question_Profile(
                            profile=request.user.profile,
                            question=q,
                            increment=1,
                            remaining=0
                        ).save()

                data = {'success': f"Successfully subscribed to course {course_title}"}
            else:
                date = {'success': f"Already subscribed to course {course_title}"}
        elif operation == 0: 
            # unsubscribe 
            print('unsubscribe')
            if CourseSubscription.objects.filter(
                profile=request.user.profile,
                course_id=course_id
            ).count() == 0:
                data = {'success': f"You are not subscribed to this course"}
            else:
                CourseSubscription.objects.filter(
                    profile=request.user.profile,
                    course_id=course_id
                ).delete()
                data = {'success': f"You have been removed from the course {course_title}"}
                # don't worry about deleting the Question_Profile records. If user not subscribed, 
                # they are ignored. But if user resubscribed, they can be re-used! :) 
        return JsonResponse(data)

class PracticeView(View):   
    def get(self, request,course_id):    
        # Get the ids of the questions for this course
        course = Course.objects.get(id=course_id)
        course_question_ids = list(
            course.questions.all().values_list(
                    'id', flat=True))
        print(f"course questions: {course_question_ids}")
        # only get the questions of that set with remaining = 0 (retrieved from Question_Profile)
        remaining_zero_questions = Question_Profile.objects.filter(
            profile=request.user.profile, 
            remaining=0,
            question_id__in=course_question_ids
        )
        print(f"Remaining 0 question: {remaining_zero_questions.values_list('id')}")
        if remaining_zero_questions.count() > 0:
            question = remaining_zero_questions[0].question
        else:
            question = None 

        # this way, you can send one at a time, and when the page refreshes, 
        # it will go to the next question with remaining = 0
        return render(
            request, 
            template_name='practice.html', 
            context={'question': question,'course': course, 'title': 'Practice'}
        )

class SignUpView(CreateView): 
    form_class = UserCreationForm
    template_name='registration/signup.html'
    success_url='/'
    def form_valid(self, form): 
        user = form.save()
        login(self.request,user)
        return redirect('/courses')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context 

class RenderQuestionView(View): 
    # Render question 
    def generate_instance(self, q=None):  
        # init result dictionary 
        result = {
            'instance': {},
            'error': {}
        } 
        cctx = q.code_context
        code = q.code 
        qtmplt = q.question_template
        atmplt = q.answer_template 
        seed = random.randint(1,100)
        print(f'Random seed generated: {seed}')
        try: 
            # seed = random.randint()
            # generate and apply random seed here ;  
            # random.seed(seed)
            # FIXME: store seed in database 
            # using that random seed, you can create the same question
            random.seed(seed)
            exec(code)
            cctx = eval(cctx) # now a dictionary with values set by code
            print(f"rendered context: {cctx}")
            # Get all elements wrapped in {{}}
            regex_pattern = re.compile(r'{{.*?}}')
            qtmplt_vars = re.findall(regex_pattern,qtmplt)
            # replace these vars with their values 
            # initialize qinst with qtmplt 
            qinst = qtmplt 
            for var in qtmplt_vars:
                var_name = re.findall(re.compile(r'{{(.*)}}'), var)[0]
                var_value = cctx[var_name] 
                qinst = qinst.replace(
                    f'{{{{{var_name}}}}}', f'{var_value}'
                    )
                # do the same thing for answer template
            atmplt_vars = re.findall(regex_pattern,atmplt)
            # initialize ainst with atmplt 
            ainst = atmplt 
            for var in atmplt_vars:
                var_name = re.findall(re.compile(r'{{(.*)}}'), var)[0]
                # get the value of variable from code execution
                var_value = cctx[var_name] 
                # answer instance built by replacing 
                # patterns with their values from code execution
                ainst = ainst.replace(
                    f'{{{{{var_name}}}}}', f'{var_value}'
                    )  
            result['instance']['question'] = qinst
            # send the seed back so the seed can be resubmitted 
            # to generate the same question/answer on check answer     
            result['instance']['seed'] = seed 
        except Exception as e:
            result['error']['Exception'] = str(e)   
        # remove error from dict if empty 
        for k in ['instance', 'error']: 
            if not result[k]:
                result.pop(k)
        return result    

    def get(self, request, qid, instances=1):
        try:    
            q = Question.objects.get(id=qid)   
            question_instances = [] 
            for i in range(instances): 
                question_instances.append(
                    self.generate_instance(q=q)
                )
            result = {
                'success': {
                    'instances' : question_instances 
                }
            }  
        except Exception as e: 
            print(e)
            result = {
                'error': str(e)
            } 
        return JsonResponse(result)

class CheckAnswerView(View): 
    def check_answer(self, request=None, q=None, answer=None, random_seed=None): 
        """ Method to get the answer to a question instance given the context and question ID """   
        result = {
            'success': {},
            'error': {}
        }
        cctx = q.code_context
        code = q.code  
        atmplt = q.answer_template 
        print(f"Random seed received: {random_seed}") 
        print(q.id)
        print(q.question_template)
        try:  
            random.seed(int(random_seed))
            exec(code)
            # now a dictionary with values set by code 
            # (same as original set by render_question thanks to random seed)
            cctx = eval(cctx) 
            print(f'checking answer rendered context: {cctx}')
            # Get all elements wrapped in {{}}
            regex_pattern = re.compile(r'{{.*?}}') 
            # do the same thing for answer template
            atmplt_vars = re.findall(regex_pattern,atmplt)
            # initialize ainst with atmplt 
            ainst = atmplt 
            for var in atmplt_vars:
                var_name = re.findall(re.compile(r'{{(.*)}}'), var)[0]
                # get the value of the variable from the seed-driven context
                var_value = cctx[var_name] 
                # answer instance built by replacing 
                # patterns with their values from code execution
                ainst = ainst.replace(
                    f'{{{{{var_name}}}}}', f'{var_value}'
                    )  
            result['success']['is_correct'] = (answer == ainst)
            try:
                qp = Question_Profile.objects.get(
                    question=q,
                    profile=request.user.profile
                ) 
                if answer == ainst: 
                    # correct  ; increment remaining by increment then increment increment lol
                    qp.remaining += qp.increment
                    # need to find optimal constant (constant = re-exposure delay)
                    # someone gets it wrong, then for OTHER students use *= 1.5
                    qp.increment += 1 
                    qp.save()
                else: 
                    qp.remaining = 1 # 
                    qp.increment = 1 
                    qp.save()  
                result['success']['correct_answer'] = ainst 
                result['success']['your_answer'] = answer 
                next_msg = (
                    f"We will ask you a similar question in {qp.remaining} days"
                ) if qp.remaining > 1 else (
                    f"We will ask you a similar question in {qp.remaining} day"
                )
                result['success']['next_msg'] = f"We will ask you a similar question in {qp.remaining} days"
            except Exception as e: 
                result['error']['Exception'] = str(e) 
        except Exception as e:
            result['error']['Exception'] = str(e) 
        # remove error from dict if empty 
        for k in ['success', 'error']: 
            if not result[k]:
                result.pop(k)
        return result 

    def post(self, request):
        qid = request.POST.get('qid',None)
        # get the same seed that was used to generate the question instance 
        random_seed = request.POST.get('seed', None) 
        q = Question.objects.get(id=qid)
        answer = request.POST.get('answer')
        result = self.check_answer(q=q, request=request, answer=answer,random_seed=random_seed)
        return JsonResponse(result)