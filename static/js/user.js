$(document).ready(function() {

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

    $("#li-answers").css("background-color", "#f2f7f6");

    $('#nav-answers').on('click',function(){
        $("#li-answers").css("background-color", "#f2f7f6");
        $("#li-experiences").css("background-color", "#FFFFFF");
        $("#li-questions").css("background-color", "#FFFFFF");
        $("#li-event-guiding").css("background-color", "#FFFFFF");
        $("#li-event-going").css("background-color", "#FFFFFF");
        $('#section-answers').show();
        $('#section-experiences').hide();
        $('#section-questions').hide();
        $('#section-event-guiding').hide();
        $('#section-event-going').hide();
    });

    $('#nav-experiences').on('click',function(){
        $("#li-answers").css("background-color", "#FFFFFF");
        $("#li-experiences").css("background-color", "#f2f7f6");
        $("#li-questions").css("background-color", "#FFFFFF");
        $("#li-event-guiding").css("background-color", "#FFFFFF");
        $("#li-event-going").css("background-color", "#FFFFFF");
        $('#section-answers').hide();
        $('#section-experiences').show();
        $('#section-questions').hide();
        $('#section-event-guiding').hide();
        $('#section-event-going').hide();
    });

    $('#nav-questions').on('click',function(){
        $("#li-answers").css("background-color", "#FFFFFF");
        $("#li-experiences").css("background-color", "#FFFFFF");
        $("#li-questions").css("background-color", "#f2f7f6");
        $("#li-event-guiding").css("background-color", "#FFFFFF");
        $("#li-event-going").css("background-color", "#FFFFFF");
        $('#section-answers').hide();
        $('#section-experiences').hide();
        $('#section-questions').show();
        $('#section-event-guiding').hide();
        $('#section-event-going').hide();
    });

    $('#nav-event-guiding').on('click',function(){
        $("#li-answers").css("background-color", "#FFFFFF");
        $("#li-experiences").css("background-color", "#FFFFFF");
        $("#li-questions").css("background-color", "#FFFFFF");
        $("#li-event-guiding").css("background-color", "#f2f7f6");
        $("#li-event-going").css("background-color", "#FFFFFF");
        $('#section-answers').hide();
        $('#section-experiences').hide();
        $('#section-questions').hide();
        $('#section-event-guiding').show();
        $('#section-event-going').hide();
    });

    $('#nav-event-going').on('click',function(){
        $("#li-answers").css("background-color", "#FFFFFF");
        $("#li-experiences").css("background-color", "#FFFFFF");
        $("#li-questions").css("background-color", "#FFFFFF");
        $("#li-event-guiding").css("background-color", "#FFFFFF");
        $("#li-event-going").css("background-color", "#f2f7f6");
        $('#section-answers').hide();
        $('#section-experiences').hide();
        $('#section-questions').hide();
        $('#section-event-guiding').hide();
        $('#section-event-going').show();
    });

});
