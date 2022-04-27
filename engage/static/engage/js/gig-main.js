$(document).ready(function() {
    $('#gigs-table').DataTable();
});
function payNow(id) {
    $.get( `/engage/create-gig-payment-link/${id}/`, function( data ) {
        data = data.data
        var options = {
        "key": "rzp_test_5CckIxrVOGTexZ",
        "amount": data.amount,
            "currency": "INR",
        "name": "Gig Payment",
        "description": "Gig Payment for ID",
        "order_id": data.id,
        "prefill": {
          "name": data.user_data.name,
          "email": data.user_data.email,
          "contact": data.user_data.contact
            },
            "handler": function (response) {
            response["gig_id"] = id
            var verify_payment = $.post('/engage/gig-payment-done/', response);
            verify_payment.done(function(data) {
                console.log(data);
            });
            verify_payment.fail(function () {
                
            });
    },
        "theme": {
          "color": "#E1507E"
        }
      };
      var rzp1 = new Razorpay(options);
      rzp1.open();
    });
}

function settleNow(id) {
    $.get(`/engage/transfer-finished-amount/${id}/`, function (data) {
        alert('Success!')
    })
}