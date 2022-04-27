$("#autocomplete").prop("disabled", true);

$.get("/api/names", function (data) {
    $("#trading_ld").fadeOut();
    symbol_list = JSON.parse(data);
    $("#autocomplete").prop("disabled", false);
    var names = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        local: symbol_list,
      });
    
    $('#autocomplete').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },{
        name: 'symbol',
        source: names,
    });
});


$("#type").change(function () {
    var type = this.value;
    if (type == 'Spot') {
        $("#expiry-date").prop("disabled", true);
        $("#strike").prop("disabled", true);
        $("#call_put").prop( "disabled", true );
    }
    else if (type == 'Futures') {
        $("#expiry-date").prop("disabled", false);
        $("#strike").prop("disabled", true);
        $("#call_put").prop( "disabled", true );
    }
    else {
        $("#expiry-date").prop("disabled", false);
        $("#strike").prop("disabled", false);
        $("#call_put").prop( "disabled", false );
    }
});

function downloadCSV(csvStr, filename) {

    var hiddenElement = document.createElement('a');
    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csvStr);
    hiddenElement.target = '_blank';
    hiddenElement.download = `${filename.toLowerCase()}.csv`;
    hiddenElement.click();
}

$("#download-form").submit(function (e) {
    e.preventDefault();
    $(".download-loading").fadeIn();
    var post_data = {
        "data_type": $("#type").val(),
        "ticker": $("#autocomplete").val(),
        "expiry_date": $("#expiry-date").val(),
        "from_date": $("#from-date").val(),
        "to_date": $("#to-date").val(),
        "interval": $("#interval").val(),
        "strike": $("#strike").val(),
        "cepe_ind": $("#call_put").val(),
    };
    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify(post_data),
        success: function (data) {
            downloadCSV(data, post_data.ticker);
            $(".download-loading").fadeOut();
        },
        error: function (xhr, textStatus, error) {
            $(".download-loading").fadeOut();
            alert("Some error occured while fetching your download, please try later.")
        },
        processData: false,
        crossDomain: true,
        type: 'POST',
        // method: 'POST',
        url: 'https://srirajk.herokuapp.com/datadownload'
    });
});

