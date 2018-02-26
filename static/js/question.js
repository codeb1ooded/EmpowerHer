$(document).ready(function() {
    $('.upvote-answer').click(function(){
        var ansid, oldstate, newstate;
        ansid = $(this).attr("data-ansid");
        oldstate = $(this).attr("data-state");
        if (oldstate === "False") {
            $(this).addClass('upvoted-button').removeClass('upvote-button');
            newstate =  "True";
            $(this).attr('data-state', "True");
            $('#text-' + ansid).html("Upvoted");
        }
        else {
            $(this).addClass('upvote-button').removeClass('upvoted-button');
            newstate = "False";
            $(this).attr('data-state', "False");
            $('#text-' + ansid).html("Upvote");
        }
        $.get('/upvote_answer/', {answer_id: ansid, state: newstate, username: username}, function(data){
            $('#upvote-' + ansid).html(data);
        });
    });
    $('.answer-button').click(function(){
        if(answer_area_exist){
            $('.answer').remove();
        }
        else{
            $(this).after('<div class="answer"><textarea type="text" rows="7" id="write-answer">' + answer + '</textarea><div class="submit"><div class="submit-answer-button"> Submit </div></div></div>');
        }
        answer_area_exist = !answer_area_exist;
    });
    $('body').on('click', '.submit-answer-button', function() {
        answer = $("#write-answer").val();
        $.get('/submit_answer/', {question_id: question_id,
                                  answer_id: answer_id, answer: answer}, function(data){
              answer_id = data;
              $('.answer').remove();
              alert("Your answer has been submitted");
        });
    });
});
