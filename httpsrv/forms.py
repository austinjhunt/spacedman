from django import forms
import json 
import string
import random
import boto3 
from django.conf import settings   
from .models import * 
from .aws.usage_plan import create_and_add_api_key_to_usage_plan
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

example_question = Question.objects.get(id=1)
class CreateQuestionForm(forms.Form): 
    question_template = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
            'placeholder': example_question.question_template
            }
        )
    )
    answer_template = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
            'placeholder': example_question.answer_template}
        )
    )
    code = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'python code that generates values for context variables my_len, my_num and my_bin', 
            }
        ),
        help_text="Use four spaces for tabs; tab key will navigate to next input"
    )
    code_context = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control',
            'placeholder': example_question.code_context}
        )
    ) 
    subject_area = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control bg-light text-dark',
            'placeholder': example_question.subject_area}
        )
    ) 

class UserCreationForm(UserCreationForm):
    """ Extension of the user creation form to generate random API keys for use with AWS API Gateway """
    account_type = forms.ChoiceField(
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        choices=[
        ('instructor', 'Instructor'), 
        ('student', 'Student')
    ]) 
    username = forms.CharField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password1 = forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder': 'Password'
    })
    password2 = forms.PasswordInput(attrs={
        'class':'form-control', 'placeholder': 'Confirm password'
    })
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "account_type")
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save()
        if commit:
            # Create two separate API keys for profile
            read_api_key = self.generate_random_string(128)
            # create,update,delete
            cud_api_key = self.generate_random_string(128) 
            # Create & save a Profile object for User 
            Profile(
                user=user,
                account_type=self.cleaned_data['account_type'],
                cud_api_key=cud_api_key,
                read_api_key=read_api_key
            ).save()

            for operation, api_key in {
                'read': read_api_key, 
                'cud': cud_api_key}.items():  
                # Create API key in AWS and add to usage plan
                # (utility function in httpsrv/aws/usage_plans.py)
                response = create_and_add_api_key_to_usage_plan(
                    user=user, key_value=api_key, operation=operation
                )
            print(response)
            
        return user

    def generate_random_string(self, strlen): 
        """ Method to generate a random string of characters of a specified length
        args:
        strlen (int) number of characters in random string 
        """
        nums = [random.choice(string.digits) for i in range(30)] 
        lower = [random.choice(string.ascii_lowercase) for i in range(30)] 
        upper = [random.choice(string.ascii_uppercase) for i in range(30)] 
        combo = nums + lower + upper 
        return ''.join(random.choice(combo) for i in range(strlen))
     