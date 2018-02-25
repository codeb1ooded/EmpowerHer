$(document).ready(function() {

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
