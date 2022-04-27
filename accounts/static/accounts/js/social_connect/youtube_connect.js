$('#yt-loading').hide();
$('#yt-warning').hide();
$('#yt-success').hide();
console.log("YEHEHHE")
$("#youtube-connect-button").on("click", function() {
    var form = $("#youtube-connect-form"),
        url = form.attr('action');
    $.get(url, function(data) {
        window.open(data['auth_url'], '_blank');
    });

});

// // Submit youtube form using jquery 
// /* attach a submit handler to the form */
$("#youtube-connect-form").submit(function(event) {
    $("#youtube-connect-btn").prop("disabled", true);
    $('#yt-warning').hide();
    $('#yt-loading').fadeIn();
    // /* stop form from submitting normally */
    event.preventDefault();

    // /* get the action attribute from the <form action=""> element */
    var $form = $(this),
        url = $form.attr('action');
    //
    var posting = $.post(url, $form.serialize());

    // /* Alerts the results */
    posting.done(function(data) {
        $('#yt-loading').fadeOut();
        $('#yt-success').fadeIn();
        $("#youtube-connect-button").prop("disabled", true);
        // $("#youtube-connect-button").attr('class', 'btn btn-square btn-success');
        $("#youtube-connect-button").html('<i class="fas fa-check"></i>');
    });
    posting.fail(function() {
        $("#youtube-connect-btn").prop("disabled", false);
        $('#yt-loading').fadeOut();
        $('#yt-warning').fadeIn();
        $('#result').text('failed');
    });
});