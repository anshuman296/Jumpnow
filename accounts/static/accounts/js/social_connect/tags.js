var tags = [];
var tagWrapper = $(".tags");

function add_tag_to_ui(value) {
    tags.push(value);
    var tag = $(`<li class="flex-item"> ${value} </li>`);
    var remove_tag = $(' <span class="close-tag text-white my-auto"> <i class="fa fa-times"></i> </span>');
    remove_tag.click(function () {
        var index = tags.indexOf($(this).parent().text().trim());
        if (index > -1) {
            tags.splice(index, 1);
        }
        $(this).parent().remove();
    });
    tag.append(remove_tag);
    tagWrapper.append(tag);
    return true;
}

$(document).ready(function () {
    $.get( "/connect/tags", function( data ) {
        var existing_tags = data['tags']
        existing_tags.forEach(function (single_tag) {
            add_tag_to_ui(single_tag);
        });
    });
    $('#connect-tags').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            if(tags.indexOf(this.value) === -1 && this.value.length > 0) {
                add_tag_to_ui(this.value);
                $(this).val('');
            }
            else {
                alert("Already used this hashtag");
            }
        }
    });

    $('#done-button').on('click', function () {
        $.ajax({
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken'),
            },
            data: JSON.stringify({"new_tags":tags}),
            dataType: 'json',
            success: function(data){
                console.log(data);
                window.location.href = '/dashboard';
            },
            error: function(xhr, status, error) {
                var err = eval("(" + xhr.responseText + ")");
                console.log(err.Message);
            },
            processData: false,
            type: 'POST',
            url: '/connect/tags'
        });
    })
});