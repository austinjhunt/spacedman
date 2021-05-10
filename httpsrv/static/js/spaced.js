var CREATE_QUESTION_ENDPOINT,
    RENDER_QUESTION_ENDPOINT,
    CHECK_ANSWER_ENDPOINT,
    GET_ANSWER_ENDPOINT,
    AKCUD, AKREAD, CSRFTOKEN;
$(document).ready(function() {
    $('.toast').toast({
        delay: 4000
    });

    //practice.html
    try {
        $('.render-question-onload').each(function(i, el) {
            // get the question id to render 
            var qid = $(el).data('render-qid');
            render_question_instance_local(qid, $(el).attr('id'));
        });
    } catch (error) {
        console.log(error);
    }

    // courses.html 
    $("#search-courses-input").on('keyup', function() {
        var val = $(this).val();
        if (val == "") {
            $(".available-course").fadeIn();
        } else {
            $("#course_list").find(".available-course").each(function(i, el) {
                if (!$(el).text().toLowerCase().includes(val)) {
                    $(el).fadeOut();
                } else {
                    $(el).fadeIn();
                }
            })
        }
    });

});

function create_question() {
    var qtmp, atmp, code, codectx, subject_area;
    subject_area = $("#id_subject_area").val();
    qtmp = $("#id_question_template").val();
    atmp = $("#id_answer_template").val();
    code = $("#id_code").val();
    codectx = $("#id_code_context").val();
    var data = {
        "question_template": qtmp,
        "answer_template": atmp,
        "code": code,
        "code_context": codectx,
        "subject_area": subject_area
    };
    $.ajax({
        type: 'POST',
        url: CREATE_QUESTION_ENDPOINT,
        data: JSON.stringify(data),
        crossDomain: true,
        headers: {
            "X-Api-Key": AKCUD,
            "Content-Type": "application/json",
        },
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function show_questions(subject_area) {
    console.log(subject_area);
    $('.question-button').fadeOut();
    var className = '.question-button.subject-' + subject_area;
    var classNameInfo = '.info-' + subject_area;
    $(className).fadeIn();
    $(classNameInfo).fadeIn();
}

function render_question_instance_aws(qid = 1, htmlElementId = null) {
    // qid is required (id of question to render) 
    // htmlElementId = optional id of element to place question text 
    $.ajax({
        type: 'GET',
        url: RENDER_QUESTION_ENDPOINT,
        data: {
            'qid': qid,
            'instances': 1,
        },
        crossDomain: true,
        headers: {
            "X-Api-Key": AKREAD,
            "Content-Type": "application/json",
        },
        success: function(response) {
            var instances = response['result']['success']['instances'];
            for (let i = 0; i < instances.length; i++) {
                // create a div for question instance
                var obj = instances[i]['instance'];
                var question;
                question = obj['question'];
                $('#' + htmlElementId).text(question);
            }
        }
    });
}

function render_question_instance_local(qid = 1, questionElementId = null) {
    // qid is required (id of question to render) 
    // htmlElementId = optional id of element to place question text 
    $.ajax({
        type: 'GET',
        url: '/render-question/' + qid + '/1',
        success: function(response) {
            console.log(response)
            var instances = response['success']['instances'];
            for (let i = 0; i < instances.length; i++) {
                // create a div for question instance
                var obj = instances[i]['instance'];
                var question, seed;
                question = obj['question'];
                seed = obj['seed'];
                console.log(seed);
                $('#' + questionElementId).text(question);
                // set the hidden random seed to send back 
                // to re-generate the exact same context 
                // that defines the same question and correct answer 
                $('#seed').val(seed);
            }
        }
    });
}


function render_instances_instructor(qid, button) {
    var instances = [];
    $.ajax({
        type: 'GET',
        url: RENDER_QUESTION_ENDPOINT,
        data: {
            'qid': qid,
            'instances': 5,
        },
        crossDomain: true,
        headers: {
            "X-Api-Key": AKREAD,
            "Content-Type": "application/json",
        },
        success: function(response) {
            var instances = response['result']['success']['instances'];
            var qinstances_div = document.createElement('div');
            var qinstances_help = document.createElement('p');
            qinstances_help.style.margin = '0.2rem';
            qinstances_help.textContent = 'click a question instance to view the answer';
            qinstances_div.className = 'qinstances-qid-' + qid;
            qinstances_div.append(qinstances_help);
            $('.' + qinstances_div.className).remove();
            qinstances_div.style.display = 'none';
            $(button).after(qinstances_div);
            for (let i = 0; i < instances.length; i++) {
                // create a div for question instance
                var obj = instances[i]['instance'];
                var context, question, answer;
                context = obj['context'];
                question = obj['question'];
                answer = obj['answer'];
                var qinst_button = document.createElement('button');
                qinst_button.className = 'btn btn-md btn-info m-2';
                let qinst_question_p = document.createElement('p');
                qinst_question_p.textContent = 'QUESTION: ' + question;
                $(qinst_question_p).css({ 'margin': "0.2rem" });
                $(qinst_question_p).addClass('qid-' + qid + '-question-qinst-' + i);
                let qinst_answer_p = document.createElement('p');
                qinst_answer_p.textContent = 'ANSWER: ' + answer;
                $(qinst_answer_p).addClass('qid-' + qid + '-answer-qinst-' + i);
                $(qinst_answer_p).css({ 'margin': "0.2rem", "display": "none" });
                $(qinst_button).on('click', function() {
                    // when clicked, hide question and show answer and change color 
                    $('.qid-' + qid + '-answer-qinst-' + i).css({
                        'width': $($('.qid-' + qid + '-question-qinst-' + i)[0]).width()
                    });
                    $(this).toggleClass('btn-info btn-success');
                    if ($(this).hasClass('btn-success')) {
                        //show answer   
                        $(qinst_question_p).fadeOut();
                        $(qinst_answer_p).fadeIn();
                    } else {
                        //show question 
                        $(qinst_question_p).fadeIn();
                        $(qinst_answer_p).fadeOut();
                    }
                })
                qinst_button.appendChild(qinst_question_p);
                qinst_button.appendChild(qinst_answer_p);
                $(qinstances_div).append(qinst_button);
            }
            $(qinstances_div).fadeIn();
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function show_add_question_modal() {
    $("#create_question_modal").modal('show');
}

function add_question_template_to_course() {
    // add the form submission from the add question modal to the course form 
    // as a new question 
    var subject_area = $("#id_subject_area").val();
    var qtmplt = $("#id_question_template").val();
    var atmplt = $("#id_answer_template").val();
    var code = $("#id_code").val();
    var cctx = $("#id_code_context").val();
    console.log(subject_area, qtmplt, atmplt, code, cctx);

    // get current number of questions in course 
    var current_num_questions = $(".course-question-input").length;
    console.log(current_num_questions);

    var new_question_index = current_num_questions + 1;

    // clone the clonable question input 
    var clone = $("#clonable-question-input").clone().addClass(
        'course-question-input').attr('id', 'course-question-' + new_question_index);
    console.log(clone);
    // update clone input values with those from modal submission
    $($(clone).find('.clonable-question-index')[0]).text(new_question_index);
    var subject_area_input = $(clone).find('.clonable-subject-area-input')[0]; //).val(subject_area);
    var qtmplt_input = $(clone).find('.clonable-question-template-input')[0]; //).val(qtmplt);
    var atmplt_input = $(clone).find('.clonable-answer-template-input')[0]; //).val(atmplt);
    var code_input = $(clone).find('.clonable-code-input')[0]; //).val(code);
    var cctx_input = $(clone).find('.clonable-code-context-input')[0]; //).val(cctx); 

    var hidden_index_input = $(clone).find('.clonable-hidden-question-index-input')[0];
    $(hidden_index_input).attr('name', 'hidden-question-index-' + new_question_index);
    $(hidden_index_input).val(new_question_index);
    // add event listener for remove question button 
    var rm_question_button = $(clone).find('.clonable-remove-question-button')[0];
    console.log(rm_question_button);
    $(rm_question_button).on('click', function() {
        // remove this question 
        $("#course-question-" + new_question_index).remove();
        // don't worry about indices 
    });


    // set the name prefix for all input names on new question 
    var name_prefix = 'question-' + new_question_index + '-';
    // set the name and value 
    $(subject_area_input).attr('name', name_prefix + 'subject-area').val(subject_area);
    $(qtmplt_input).attr('name', name_prefix + 'question-template').val(qtmplt);
    $(atmplt_input).attr('name', name_prefix + 'answer-template').val(atmplt);
    $(code_input).attr('name', name_prefix + 'code').val(code);
    $(cctx_input).attr('name', name_prefix + 'code-context').val(cctx);

    // append new question to course_questions list 
    $("#course_questions").append(clone);
    $(clone).removeClass('d-none');

    $("#create_question_modal").modal('hide');
}

function subscribe_to_course(course_id, operation = 1) {
    $.ajax({
        url: '/subscribe/' + course_id + '?op=' + operation,
        method: 'GET',
        success: function(response) {
            var msg = response['success'];
            var body = $("#subscribed-to-course-toast").find('.toast-body')[0];
            $(body).text(msg);
            $("#subscribed-to-course-toast").css({ 'z-index': '20' });
            $(".subscribed-toast").toast('show');
            setTimeout(function() {
                window.location.reload();
            }, 4000);

        },
        error: function(error) {
            alert(error);
        }
    })
}

function check_answer(qid) {
    $.ajax({
        url: '/check-answer/',
        method: 'POST',
        data: {
            'qid': qid,
            'answer': $("#question-" + qid + "-answer").val(),
            'seed': $("#seed").val(),
            'csrfmiddlewaretoken': CSRFTOKEN
        },
        success: function(response) {
            console.log(response);
            var is_correct = response['success']['is_correct'];
            var next_msg = response['success']['next_msg'];
            console.log(is_correct);
            if (!is_correct) {
                var correct_answer = response['success']['correct_answer'];
                var your_answer = response['success']['your_answer'];
                var incorrect_html = `
                <p>Incorrect</p>
                <p>You said: ` + your_answer + `</p>
                <p>The correct answer is: ` + correct_answer + `</p>
                <p>` + next_msg + '</p>';
                $(".incorrect").html(incorrect_html);
                $(".answer-form").fadeOut();
                $(".incorrect").fadeIn();
                $(".check-answer-button").fadeOut();
                $(".next-question-button").fadeIn();
            } else {
                var correct_html = `
                <p>Great work! Your answer was correct.</p>
                <p>` + next_msg + '</p>';
                $(".correct").html(correct_html);
                $(".answer-form").fadeOut();
                $(".correct").fadeIn();
                $(".check-answer-button").fadeOut();
                $(".next-question-button").fadeIn();
            }
        },
        error: function(error) {
            console.log(error);
        }
    })
}