$('#fb-loading').hide();
$('#fb-warning').hide();
$('#fb-success').hide();

$("#facebook-connect-button").on("click", function () {
    $('#facebook-connect-modal').modal('show');
});

// Submit instagram form using jquery
/* attach a submit handler to the form */
$("#facebook-connect-form").submit(function (event) {
    $("#facebook-connect-btn").prop("disabled", true);
    $('#fb-warning').hide();
    $('#fb-loading').fadeIn();
/* stop form from submitting normally */
event.preventDefault();

/* get the action attribute from the <form action=""> element */
var $form = $(this),
    url = $form.attr('action');

var posting = $.post(url, $form.serialize());

/* Alerts the results */
    posting.done(function(data) {
        $('#fb-loading').fadeOut();
        $('#fb-success').fadeIn();
        $("#facebook-connect-button").prop("disabled", true);
        // $("#facebook-connect-button").attr('class', 'btn btn-square btn-success');
        $("#facebook-connect-button").html('<i class="fas fa-check"></i>');
    });
    posting.fail(function () {
        $("#facebook-connect-btn").prop("disabled", false);
        $('#fb-loading').fadeOut();
        $('#fb-warning').fadeIn();
        $('#result').text('failed');
    });
});