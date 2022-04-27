$("#contact-form").submit(function(e) {
    $("#loading-div").fadeIn();
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               $("#loading-div").fadeOut();
               $("#response-div").fadeIn();
           }
         });
});