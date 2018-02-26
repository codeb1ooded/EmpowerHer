$(document).ready(function() {

    $('.user-going-button').click(function(){
        var oldstate, newstate;
        var event_id, prefix;
        oldstate = $(this).attr("data-state");
        event_id = $(this).attr("data-event-id");
        prefix = $(this).attr("data-event");
        if (oldstate === "False") {
            $(this).addClass('going-guided-button').removeClass('going-guide-button');
            newstate =  "True";
            $(this).attr('data-state', "True");
            $('#' + prefix + '-going-text-' + event_id).html("I am going!");
        }
        else {
            $(this).addClass('going-guide-button').removeClass('going-guided-button');
            newstate = "False";
            $(this).attr('data-state', "False");
            $('#' + prefix + '-going-text-' + event_id).html("Are you going?");
        }
        $.get('/going_event/', {event_id: event_id, state: newstate, username: username}, function(data){});
    });
    $('.user-guide-button').click(function(){
        var oldstate, newstate;
        var event_id, prefix;
        oldstate = $(this).attr("data-state");
        event_id = $(this).attr("data-event-id");
        prefix = $(this).attr("data-event");
        if (oldstate === "False") {
            $(this).addClass('going-guided-button').removeClass('going-guide-button');
            newstate =  "True";
            $(this).attr('data-state', "True");
            $('#' + prefix + '-guide-text-' + event_id).html("I am a guide!");
        }
        else {
            $(this).addClass('going-guide-button').removeClass('going-guided-button');
            newstate = "False";
            $(this).attr('data-state', "False");
            $('#' + prefix + '-guide-text-' + event_id).html("Are you guiding?");
        }
        $.get('/guiding_event/', {event_id: event_id, state: newstate, username: username}, function(data){});
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

});
