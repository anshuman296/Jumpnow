$("#reg-loading").hide();
$("#reg-form").validate({
        rules : {
          first_name : {
            required: true,
          },
          last_name : {
            required: true,
          },
          email : {
            required: true,
            email: true,
          },
          password1 : {
            required: true,
          },
          password2 : {
            required: true,
            equalTo: "#id_password1",
          },
          mobile_number: {
            required: true,
            maxlength: 10,
            minlength: 10,
            digits: true
        },
        privacy: {
              required: true, 
          }
        },
        messages : {
          mobile_number: {
            required: "This field is required",
            maxlength: "Please enter a 10 digit phone number",
            minlength: "Please enter a 10 digit phone number",
            digits: "Only numbers are allowed"
          },
          password2 : {
            required: "This field is required",
            equalTo: "The passwords do not match."
            },
            privacy: {
              required: '',
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