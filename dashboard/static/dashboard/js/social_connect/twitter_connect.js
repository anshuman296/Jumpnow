$('#it-loading').hide();
$('#it-warning').hide();
$('#it-success').hide();

$("#twitter-connect-button").on("click", function () {
    $('#twitter-connect-modal').modal('show');
});

// Submit twitter form using jquery
/* attach a submit handler to the form */
$("#twitter-connect-form").submit(function (event) {
    $("#twitter-connect-btn").prop("disabled", true);
    $('#it-warning').hide();
    $('#it-loading').fadeIn();
/* stop form from submitting normally */
event.preventDefault();

/* get the action attribute from the <form action=""> element */
var $form = $(this),
    url = $form.attr('action');

var posting = $.post(url, $form.serialize());

/* Alerts the results */
    posting.done(function(data) {
        $('#it-loading').fadeOut();
        $('#it-success').fadeIn();
        $("#twitter-connect-button").prop("disabled", true);
        // $("#twitter-connect-button").attr('class', 'btn btn-square btn-success');
        $("#twitter-connect-button").html('<i class="fas fa-check"></i>');
    });
    posting.fail(function () {
        $("#twitter-connect-btn").prop("disabled", false);
        $('#it-loading').fadeOut();
        $('#it-warning').fadeIn();
        $('#result').text('failed');
    });
});