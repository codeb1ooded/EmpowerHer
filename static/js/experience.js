function openNav() {
    document.getElementById("share-experience").style.width = "100%";
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    document.getElementById("share-experience").style.width = "0%";
}

$(document).ready(function() {
    $('.upvote-experience').click(function(){
        var expid, oldstate, newstate;
        expid = $(this).attr("data-expid");
        oldstate = $(this).attr("data-state");
        if (oldstate === "False") {
            $(this).addClass('upvoted-button').removeClass('upvote-button');
            newstate =  "True";
            $(this).attr('data-state', "True");
            $('#text-' + expid).html("Upvoted");
        }
        else {
            $(this).addClass('upvote-button').removeClass('upvoted-button');
            newstate = "False";
            $(this).attr('data-state', "False");
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
});
