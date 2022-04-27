function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}
 
function populateTable(data, table) {
      table.clear().draw();
      console.log(data);
      for (i = 0; i < data.length; i++) {
            table.row.add(
                  [`<input class="" name="infs" value="${data[i].id}" id="checkbox1" type="checkbox" data-bs-original-title="" title="">`,
                        data[i].tags,
                        data[i].jumpnow_score,
                        data[i].profiles_data[0].engagement_rate,
                        32,
                  `<a href="/discovery/influencer/${data[i].id}/"> Visit Profile </a>`]).draw();
      }
}

function populateSelect(id,data) {
      var $dropdown = $(`#${id}`);
      $.each(data, function () {
            $dropdown.append($("<option />").val(this.pk).text(this.fields.name));
      });
}

const saveData = (function () {
    const a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return function (data, fileName) {
        const blob = new Blob([data], {type: "octet/stream"}),
            url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
          a.click();
          a.remove();
        window.URL.revokeObjectURL(url);
    };
}());

$(document).ready(function () {
      $("#search-loading").hide();
      var results = $('#result_table').DataTable();
      $(".js-example-basic-multiple").select2();
      // Call a method on the slider
      $("#new-campaign-name").hide();
      $("#campaign-list-select-div").hide();
      $("#new-campaign-list-name").hide();
      // var mySlider = $("input.slider").slider();
      // var value = mySlider.slider('getValue');

      $("#export-btn").on('click', function () {
            selected = [];
            $(".results input:checked").each(function() {
                  selected.push($(this).attr('value'));
            });
            console.log(selected);
            if (selected.length == 0) {
                  alert("Please select profiles before exporting them!");
            } else {
                  export_data = ({ profiles: selected });
                  console.log(export_data);
                  $.ajax({
                        url: '/discovery/api/export-influencer-list/',
                        headers: { "X-CSRFToken": getCookie("csrftoken") },
                        type: 'post',
                        data: export_data,
                        success: function (data) {
                              saveData(data, 'test.csv');
                        },
                        error: function(xhr, status, error) {
                              console.log(error);
                        }
                  });
            }
      });

      $("#search_discovery").on('click', function () {
        $("#search-loading").fadeIn();
            var form_data = {
                  "search_term": $("#search_main").val(),
                  // "min_followers": mySlider.slider('getValue'),
                  "csrf_token": $("input[name='csrfmiddlewaretoken']").val()
            };
            var search = $.ajax({
                  headers: { "X-CSRFToken": getCookie("csrftoken") },
                  type: "POST",
                  url: '/discovery/search/',
                  data: form_data,
                  success: function (resultData) {
                        const search_data = resultData.pop();
                        var progress_bar = $("#search-progress");
                        var percent = Math.round((search_data.searches_done / search_data.searches_max) * 100);
                        progress_bar.attr({ style: `width: ${percent}%`, 'aria-valuenow': percent });
                        $("#done").html(search_data.searches_done);
                        populateTable(resultData, results);
                        $("#search-loading").fadeOut();
                  },
                  error: function (data) {
                        alert("Please subscribe to our services");
                  }
            });
            console.log(form_data);

      });

      $("#atl").on('click', function () {
            selected = [];
            $(".results input:checked").each(function() {
                  selected.push($(this).attr('value'));
            });
            if (selected.length == 0) {
                  alert("Please select profiles before adding them to the list!");
            } else {
                  $('#atlModal').modal('show');
                  $.get( "/discovery/api/get-campaigns/", function( data ) {
                        console.log(data);
                        populateSelect('campaign-select', data);
                        
                  });
            }


      });

      $('#campaign-select').on('change', function() {
            if (this.value === 'new3-campaign') {
                  $("#new-campaign-name").fadeIn();
                  $("#new-campaign-list-name").fadeIn();
                  $("#new-campaign-name").attr({"required": "required"});
                  $("#new-campaign-list-name").attr({"required": "required"});
            } else {
                  $("#new-campaign-name").fadeOut();
                  $("#new-campaign-list-name").fadeOut();
                  $("#campaign-list-select-div").fadeIn();
                  $.get( `/discovery/api/get-campaigns-list/${this.value}/`, function( data ) {
                        console.log(data);
                        populateSelect('campaign-list-select', data);
                  });
            }
      });

      $('#campaign-list-select').on('change', function() {
            if (this.value === 'new3-campaign-list') {
                  $("#new-campaign-list-name").fadeIn();
                  $("#new-campaign-list-name").attr({"required": "required"});
            } else {
                  $("#new-campaign-list-name").fadeOut();
            }
      });

      $('#atl-submit').on('click', function () {
            if ($("#list-form")[0].checkValidity()) {
                  partial_data = $('#list-form').serializeArray();
                  partial_data.push({name: "infs", value: selected});
                  console.log(partial_data, typeof(partial_data));
                  $.ajax({
                        url: '/discovery/api/create-campaign-list/',
                        type: 'post',
                        data: partial_data,
                        success: function (data) {
                              alert("Selected influencers added to list!");
                        $('#atlModal').modal('hide');
                        }
                  });
        }   
      });




} );