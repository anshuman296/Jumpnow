
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

window.onload = function () {
    function start_chart_render_process() {
        $("#chart_ld").fadeIn();
        $.ajax({
            contentType: 'application/json',
            dataType: 'json',
            success: function(data){
                $("#chart_ld").fadeOut();
                $("#warning").fadeOut();
                render_chart_from_api(data, "heatmap_chart");
            },
            error: function (err) {
            $("#chart_ld").fadeOut();
            $("#warning").fadeIn();    
            // $(".actual-chart").html(err.responseText);
        },
            processData: false,
            type: 'POST',
            url: 'http://srirajk.herokuapp.com/heatmap'
        });
    }
    start_chart_render_process();
};





function RefreshData() {
    if ($("#heatmap_chart").length) {
        notification("Chart Refresh Notification", "Please note: we refresh the chart every 5 minutes. Your chart will be get some new data in a few seconds.");
        start_chart_render_process();
    }
    else { return; }
}	


setInterval(function () { RefreshData(); }, 295000);