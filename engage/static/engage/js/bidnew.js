$(document).ready(function() {
    $('#bid-check').change(function () {
        if(this.checked) {
            $("#bid-on").fadeIn();
        }
        else {
            $("#bid-on").fadeOut();
        }      
    });
    $('#bid-start-date').datepicker({
        language: 'en',
        minDate: new Date(),
        dateFormat: 'dd-mm-yyyy',
    })
    $('#bid-end-date').datepicker({
        language: 'en',
        minDate: new Date(),
        dateFormat: 'dd-mm-yyyy',
    })
});