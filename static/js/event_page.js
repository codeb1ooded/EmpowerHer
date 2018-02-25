function openNav() {
    document.getElementById("share-experience").style.width = "100%";
}

function closeNav() {
    document.getElementById("share-experience").style.width = "0%";
}

function openAskQuestion() {
    document.getElementById("ask-question").style.width = "100%";
}

function closeAskQuestion() {
    document.getElementById("ask-question").style.width = "0%";
}

// Sticky Header
$(window).scroll(function() {
    if ($(window).scrollTop() > 100) {
        $('.main_h').addClass('sticky');
    } else {
        $('.main_h').removeClass('sticky');
    }
});

$(document).ready(function() {
    $('#going-button').click(function(){
        var oldstate, newstate;
        oldstate = $(this).attr("data-state");
        if (oldstate === "False") {
            $(this).addClass('going-guided-button').removeClass('going-guide-button');
            newstate =  "True";
            $(this).attr('data-state', "True");
            $('#going-text').html("I am going!");
        }
        else {
            $(this).addClass('going-guide-button').removeClass('going-guided-button');
            newstate = "False";
            $(this).attr('data-state', "False");
            $('#going-text').html("Are you going?");
        }
        $.get('/going_event/', {event_id: event_id, state: newstate, username: username}, function(data){});
    });
    $('#guide-button').click(function(){
        var oldstate, newstate;
        oldstate = $(this).attr("data-state");
        if (oldstate === "False") {
            $(this).addClass('going-guided-button').removeClass('going-guide-button');
            newstate =  "True";
            $(this).attr('data-state', "True");
            $('#guide-text').html("I am a guide!");
        }
        else {
            $(this).addClass('going-guide-button').removeClass('going-guided-button');
            newstate = "False";
            $(this).attr('data-state', "False");
            $('#guide-text').html("Are you guiding?");
        }
        $.get('/guiding_event/', {event_id: event_id, state: newstate, username: username}, function(data){});
    });
    $('.see-more').click(function() {
        $(this).parent().find('.question-answer').removeClass('condensed-answer');
        $(this).remove();
    });

    $('.upvote-experience').click(function(){
       var expid, oldstate, newstate;
       expid = $(this).attr("data-expid");
       oldstate = $(this).attr("data-old-state");
       if (oldstate === "False") {
           $(this).addClass('upvoted-button').removeClass('upvote-button');
           newstate =  "True";
           $(this).attr('data-old-state', "True");
           $('#text-' + expid).html("Upvoted");
       }
       else {
           $(this).addClass('upvote-button').removeClass('upvoted-button');
           newstate = "False";
           $(this).attr('data-old-state', "False");
           $('#text-' + expid).html("Upvote");
       }
       $.get('/upvote_experience/', {experience_id: expid, state: newstate, username: username}, function(data){
           $('#upvote-' + expid).html(data);
       });
    });

    $('#submit-experience-button').click(function(){
        $('#submit-experience-button').addClass('submited-button');
        experience = $("#experience-text").val();
        $.get('/submit_experience/', {event_id: event_id, experience_id: user_exp_id, experience: experience}, function(data){
            user_exp_id = data;
            $('#submit-experience-button').removeClass('submited-button');
            $("#share-experience").width(0);
            alert("Your experience has been submitted");
        });
    });

    $('#ask-button').click(function(){
        var question = $("#ask-input").val();
        $.get('/submit_question/', {event_id: event_id, question: question}, function(data){
            $("#ask-question").width(0);
            alert("Your question has been submitted");
        });
    });
});
