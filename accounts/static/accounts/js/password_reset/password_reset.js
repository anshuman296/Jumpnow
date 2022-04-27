$("#reg-loading").hide();
$("#reg-form").validate({
        rules : {
          email : {
            required: true,
            email: true,
          }
        },
        highlight: function(element, errorClass, validClass) {
            $(element).addClass("is-invalid").removeClass("is-valid");
        },
      unhighlight: function(element, errorClass, validClass) {
            $(element).addClass("is-valid").removeClass("is-invalid");
        },
        submitHandler: function (form, e) {
          $("#submit-btn").fadeOut();
          $("#reg-loading").fadeIn();

          form.submit();
        }
    });