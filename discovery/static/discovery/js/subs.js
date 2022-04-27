$("#sub-loading").fadeOut();
$("#basic-btn").click(function () {
  $("#sub-loading").fadeIn();
  var type = $("input[name='radio1']:checked").val();
  if (type == 'monthly') {
    $.get("/discovery/subscriptions/basic/monthly/", function (data) {
      console.log("IN MONTHLY");
      console.log(data);
      var options = {
        "key": "rzp_test_5CckIxrVOGTexZ",
        "subscription_id": data.id,
        "name": data.user_data.name,
        "description": "Monthly Test Plan",
        "callback_url": "http://127.0.0.1:8000/discovery/subscriptions/basic/done/monthly/",
        "prefill": {
          "name": data.user_data.name,
          "email": data.user_data.email,
          "contact": data.user_data.contact
        },
        "theme": {
          "color": "#E1507E"
        }
      };
      var rzp1 = new Razorpay(options);
      rzp1.open();
      $("#sub-loading").fadeOut();
    });
  } else if (type == 'yearly') {
    $.get( "/discovery/subscriptions/basic/yearly/", function( data ) {
      var options = {
        "key": "rzp_test_5CckIxrVOGTexZ",
        "subscription_id": data.id,
        "name": data.user_data.name,
        "description": "Monthly Test Plan",
        "callback_url": "http://127.0.0.1:8000/discovery/subscriptions/basic/done/yearly/",
        "prefill": {
          "name": data.user_data.name,
          "email": data.user_data.email,
          "contact": data.user_data.contact
        },
        "theme": {
          "color": "#E1507E"
        },
        "offer_id": "offer_HD8IItbamZ69A3"
      };
      var rzp1 = new Razorpay(options);
      rzp1.open();
      $("#sub-loading").fadeOut();
    });
  }
  
});