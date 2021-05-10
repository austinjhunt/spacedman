from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model): 
    """ extension of the User model to set an apikey for each user """
    class Meta:
        app_label = 'httpsrv'
    # CREATE/DELETE/UPDATE 
    cud_api_key = models.CharField(max_length=512, default="")
    # READ 
    read_api_key = models.CharField(max_length=512, default="") 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ACCOUNT_TYPE_CHOICES = (
        ('instructor', 'Instructor'),
        ('student', 'Student')
    )
    account_type = models.CharField(max_length=30, default='student', choices=ACCOUNT_TYPE_CHOICES)
class Question(models.Model): 
    class Meta: 
        app_label = 'httpsrv'  
    question_template = models.TextField()
    answer_template = models.TextField()
    code = models.TextField()
    code_context = models.TextField()
    subject_area = models.CharField(max_length=50, null=False, default="") 

    def validate_fields(self): 
        """ Method to validate the fields before saving. 
        Call this explicitly and save only if return is True """
        if "import os" in self.code or "import sys" in self.code:
            return False
        return True

    
class Question_Profile(models.Model): 
    """ Model mapping question template to user in order to allow many to many """
    class Meta: 
        app_label = 'httpsrv'
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    # how much to increment remaining when question answered correctly 
    increment = models.IntegerField(default=1)  
    # how much time (days, hours, minutes may be variable) 
    # before question asked again using this template 
    # ask question when remaining = 0
    remaining = models.IntegerField(default=0)

class Course(models.Model): 
    instructor = models.ForeignKey(Profile, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    course_title = models.TextField(default="")   
    
class CourseSubscription(models.Model): 
    # Student must subscribe to a course in order to get questions 
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subscription_timestamp = models.DateTimeField(auto_now=True)

# save question instances, 
# find patterns in time taken to answer 
# cluster question instances by time taken to answer 

class QuestionInstance(models.Model): 
    # Saved by the CheckAnswer lambda 
    question_template = models.ForeignKey(Question,on_delete=models.CASCADE)
    time_to_answer = models.IntegerField()
    question_text = models.TextField()
    correct_answer = models.TextField()
    submitted_answer = models.TextField()
    timestamp = models.DateTimeField()


# course model 
# student requests question from a course 
# are there any questions that have never been asked? 
# if so they are in the Question table and not Question_Profile table
# randomly choose question when generating a question for a user
#   if not asked yet then create Question_Profile
#   if already asked then increment/remaining  

# single page that takes a question id (and requesting user) 
# get me a question; sends course id and user id, returns a question displayed with input 
