# 3-21 Notes
create API that 
    1) takes user id 
    2) gets the best next question to be asked based on what they answered correctly 
create API that 
    1) accepts answers 
    2) modifies database based on answers 
create API that 
    1) accepts context and question id
    2) returns answer 


(1) login / sign up
when they login they see first question, tells them how many questions they can answer today 

how can we show that spaced repetition is effective?
after each question:
    "was this a good time for you to be asked about this?"

how fresh is this question? fresh2death? mintyfresh?

create 1) spaced rep system and 2) normal random question asker
for each question, ask: 
    is this question too early, too late, or fresh

we know from algorithm when system will present student with question
say you answer question correctly a few times in a row.. we know when you'll be prompted again based on algorithm

idea for testing: 
    don't follow algorithm every time 
    flip a coin, either use algorithm or dont
    single system with variety: sometimes ask question too early, sometimes too late, sometimes #mintyfresh

    better: 
        we should not propose algo that we have in paper 
        if you propose it, you have to justify 
        ask question anyway, answer to question "too early? too late?" will improve algorithm / system 
        for each category of question, we can determine / know the best time to ask questions 
        re-exposure delays actually calculated by students 
        dont ask "good timing? bad timing?" after every question, just some, distribute among students, randomize in clever way 
        algorithm will be based on their answers 
        we phrase as "There is an optimal re-exposure delay for each question/category... this is calculated by students"
        if you can prove that statement, you show that system works 

Before meeting:
    GOAL: want to prove that spaced rep system is better than random system 
After meeting: 
    GOAL: want to show that each topic/question has optimal re-exposure delay to demonstrate usefulness of system

To distinguish our app...
    We want to find optimal time not by asking easy? hard? etc. but by asking same question again, extract optimal re-exposure delay just by whether they answer correctly 
    When their answers go from correct -> incorrect, that indicates a threshold that could be defined as re-exposure delay 
    Risks for this type of testing: 
        1) users get all questions right 
        2) users get all questions wrong 
        3) users don't answer all questions
        4) not enough time for increments to double before submission deadline 

Results section, we may not have a lot to say; that's okay if you frame the contribution as a system for data extraction, but you can't say that data was extracted