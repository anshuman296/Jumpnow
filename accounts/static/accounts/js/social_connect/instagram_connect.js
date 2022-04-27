$('#ic-loading').hide();
$('#ic-warning').hide();
$('#ic-success').hide();

$("#instagram-connect-button").on("click", function () {
    $('#instagram-connect-modal').modal('show');
});

// Submit instagram form using jquery 
/* attach a submit handler to the form */
$("#instagram-connect-form").submit(function (event) {
    $("#instagram-connect-btn").prop("disabled", true);
    $('#ic-warning').hide();
    $('#ic-loading').fadeIn();
/* stop form from submitting normally */
event.preventDefault();

/* get the action attribute from the <form action=""> element */
var $form = $(this),
    url = $form.attr('action');

var posting = $.post(url, $form.serialize());

/* Alerts the results */
    posting.done(function(data) {
        $('#ic-loading').fadeOut();
        $('#ic-success').fadeIn();
        $("#instagram-connect-button").prop("disabled", true);
        // $("#instagram-connect-button").attr('class', 'btn btn-square btn-success');
        $("#instagram-connect-button").html(' <i class="fas fa-check"></i>');
    });
    posting.fail(function () {
        $("#instagram-connect-btn").prop("disabled", false);
        $('#ic-loading').fadeOut();
        $('#ic-warning').fadeIn();
        $('#result').text('failed');
    });
});