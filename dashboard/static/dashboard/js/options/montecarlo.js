$("#autocomplete").prop("disabled", true);
$("#strike").select2({});
$("#date").val('2010-01-01');

function notification(title, message) {
    $.notify({
      title:title,
      message:message,
   },
   {
      type:'primary',
      allow_dismiss:true,
      newest_on_top:true ,
      mouse_over:true,
      showProgressbar:false,
      spacing:10,
      timer:2000,
      placement:{
        from:'bottom',
        align:'right'
      },
      offset:{
        x:30,
        y:30
      },
      delay:1000 ,
      z_index:10000,
      animate:{
        enter:'animated flash',
        exit:'animated shake'
    }
  });
}

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

$('#autocomplete').bind('typeahead:select', function (ev, symbol) {
    $("#expiry_ld").fadeIn();
    $('#expiry').empty();
    $("#strike").empty();
    $.get(`/api/dates/${symbol}`, function (data) {
        $("#expiry_ld").fadeOut();
        var dates = JSON.parse(data);
        $("#expiry").append("<option selected disabled>Expiry Date</option>");
        $.each(dates, function() {
            $('#expiry').append($("<option />").val(this).text(this));
        });
    });
});

$("#expiry").change(function () {
    var name = $("#autocomplete").val();
    var date = this.value;
    $("#strike").empty();
    $("#strike_ld").fadeIn();
    $.get(`/api/prices/${name}/${date}`, function( data ) {
        var prices = JSON.parse(data);
        $("#strike_ld").fadeOut();
        $.each(prices, function() {
            $('#strike').append($("<option />").val(this).text(this));
        });
        $("#strike").select2({});
    });
});
function render_dual_axis_chart(data, dataset_one_name, dataset_two_name) {
    var lineChartData = {
			labels: data.labels,
			datasets: [{
				label: dataset_one_name,
				borderColor: 'red',
				backgroundColor: 'white',
				fill: false,
				data: data.dataset_1,
				yAxisID: 'y-axis-1',
			}, {
				label: dataset_two_name,
				borderColor: 'blue',
				backgroundColor: 'blue',
				fill: false,
				data: data.dataset_2,
				yAxisID: 'y-axis-2'
			}]
		};

    var ctx = $("#oi_chart");
    var myLineChart = new Chart(ctx, {
        type: "line",
        data: lineChartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            hoverMode: 'index',
            stacked: false,
            title: {
                display: true,
                text: 'Multi Axis Chart'
            },
            scales: {
                yAxes: [{
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'left',
                    id: 'y-axis-1',
                }, {
                    type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                    display: true,
                    position: 'right',
                    id: 'y-axis-2',

                    // grid line settings
                    gridLines: {
                        drawOnChartArea: false, // only want the grid lines for one axis to show up
                    },
                }],
            }
        }
    });

}

function processChartData(rawData, data1_selection, data2_selection) {
    // console.log(typeof (rawData));
    labels = [];
    dataset_one = [];
    dataset_two = [];
    for (const [key, value] of Object.entries(rawData)) {
        labels.push(key);
        for (const [key, datapoint] of Object.entries(value)) {
            if (key == data1_selection) {
                dataset_one.push(datapoint);
            }
            else if (key == data2_selection) {
                dataset_two.push(datapoint);
            }
        }
    }
    data = {
        "labels": labels,
        "dataset_1": dataset_one,
        "dataset_2": dataset_two,
    };
    return data;
}

function create_chart_canvas(id) {
    var chart_elem = `<canvas id="${id}" style="width: 100%; height: 100%;"></canvas>`;
    $(".actual-chart").append(chart_elem);
}

function render_chart_from_api(data, element_id) {
    if ($(`#${element_id}`).length) {
        $(`#${element_id}`).remove();
        create_chart_canvas(element_id);
        var ctx = document.getElementById(element_id).getContext('2d');
        var myChart = new Chart(ctx, data);
    }
    else {
        create_chart_canvas(element_id);
        var ctx = document.getElementById(element_id).getContext('2d');
        var myChart = new Chart(ctx, data);
    }
}

function start_chart_render_process() {
    $("#chart_ld").fadeIn();
    var d = new Date($("#date").val());
    var date_string = `${d.getDate()}/${d.getMonth() + 1}/${d.getFullYear()}`;
    var get_data = { "ticker": $('#autocomplete').val(), "simulation_days": parseInt($('#simulation').val()), "returns_from": date_string };
    console.log(get_data);
    $.ajax({
        contentType: 'application/json',
        data: JSON.stringify(get_data),
        dataType: 'json',
        success: function(data){
            $("#chart_ld").fadeOut();
            $("#warning").fadeOut();
            render_chart_from_api(data, "montecarlo_chart");
        },
        error: function (err) {
        $("#chart_ld").fadeOut();
        $("#warning").fadeIn();    
        // $(".actual-chart").html(err.responseText);
    },
        processData: false,
        type: 'POST',
        url: 'https://srirajk.herokuapp.com/montecarlo'
    });
}



$("#montecarlo-form").validate({
    highlight: function(element, errorClass, validClass) {
        $(element).addClass("is-invalid").removeClass("is-valid");
    },
  unhighlight: function(element, errorClass, validClass) {
        $(element).addClass("is-valid").removeClass("is-invalid");
    },
    submitHandler: function (form, e) {
        e.preventDefault();
        start_chart_render_process();
    }
});



function RefreshData() {
    if ($("#montecarlo_chart").length) {
        notification("Chart Refresh Notification", "Please note: we refresh the chart every 5 minutes. Your chart will be get some new data in a few seconds.");
        start_chart_render_process();
    }
    else { return; }
}	


setInterval(function () { RefreshData(); }, 295000);