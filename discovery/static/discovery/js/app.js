function custom_template(obj) {
    var data = $(obj.element).data();
    var text = $(obj.element).text();
    if (data && data['img_src']) {
        img_src = data['img_src'];
        template = $("<div><img src=\"" + img_src + "\" style=\"width:30px;height:30px;\"/><p style=\"font-weight: 700;font-size:14px;text-align:center;\">" + +"</p></div>");
        return template;
    }
}


var options = {
    'templateSelection': custom_template,
    'templateResult': custom_template,
}
$('#social_select').select2(options);
$('.select2-container--default .select2-selection--single').css({ 'height': '30px' });






function update() {
    var select = document.getElementById('social_select');
    var option = select.options[select.selectedIndex];
    var valueSelected = option.value;
    // var valueSelectedOne = option.value;

    const searchClient = algoliasearch('GL6G6ED5LB', 'ab8447988d6ed59f360e80c1b386d130');


    var newSubAsc;
    var newSubDesc;
    var description = "follow_Count"
    if (valueSelected === "instagram") {
        newSubAsc = "instagram_subs_asc"
        newSubDesc = "instagram_subs_desc"
    } else if (valueSelected === "youtube") {
        newSubAsc = "youtube_subs_asc"
        newSubDesc = "youtube_subs_desc"

    }







    // var newIndex = valueSelected


    const search_one = instantsearch({
        indexName: "Instagram",
        searchClient,
    })




    search_one.addWidgets([
        instantsearch.widgets.searchBox({
            container: '#input-container',
            placeholder: 'Search anything',
            showSubmit: true,
        }),
        instantsearch.widgets.searchBox({
            container: '#geo-search',
            placeholder: 'Search Location',
            showSubmit: true,
        }),

        instantsearch.widgets.hits({
            container: '#hits',
            hitsPerPage: 6,
            templates: {
                item: templateMain(),
                empty: 'we didnt find any <em>\"{{query}}"\</em>'
            }
        }),

        instantsearch.widgets.pagination({
            container: '#pagination',
            templates: {
                first: 'first',
                last: 'last',
                previous: 'prev',
                next: 'next',
            },
        }),

        instantsearch.widgets.voiceSearch({
            container: '#searchbox_two',
            additionalQueryParameters(query) {
                return {
                    ignorePlurals: false,
                };
            },
        }),
        // instantsearch.widgets.numericMenu({
        //   container: '#age',
        //   attribute: 'age',
        //   items: [
        //     { label: 'All Age' },
        //     { label: 'Less than 20y', end: 10 },
        //     { label: 'Between 20y - 25y', start: 20, end: 25 },
        //     { label: 'Between 25y-30y', start: 25 , end:30 },
        //     { label: 'More than 30y', start: 30 },
        //   ],
        // }),
        // instantsearch.widgets.rangeInput({
        //     container: '#followers_count',
        //     attribute: 'subs',
        //     min: 0,
        //     max: 500
        //
        // }),
        // instantsearch.widgets.refinementList({
        //     container: '#gender',
        //     attribute: 'gender',
        //     operator: 'and',
        // }),
        // instantsearch.widgets.refinementList({
        //     container: '#tags',
        //     attribute: 'tags',
        // }),
        // instantsearch.widgets.sortBy({
        //     container: '#followers_count_main',
        //     items: [
        //         { label: 'Followers', value: valueSelected },
        //         { label: 'Follwers ↑', value: newSubAsc },
        //         { label: 'Follwers ↓', value: newSubDesc }
        //     ]
        // }),
        // instantsearch.widgets.sortBy({
        //   container: '#name',
        //   items:     [
        //     { label: 'By Name', value:'youtube' },
        //     { label: 'Name ↑', value: 'youtube_name_asc' },
        //     { label: 'Name ↓', value: 'youtube_name_desc' }
        //   ]
        // }),
        //
        // instantsearch.widgets.rangeInput({
        //     container: '#age',
        //     attribute: 'age',
        //     min: 0,
        //     max: 70
        //
        // }),
        // instantsearch.widgets.clearRefinements({
        //     container: '#clear-refinements',
        //     includedAttributes: ['tags', 'gender', ],
        //     templates: {
        //         resetLabel: 'Reset Filters <i class="fas fa-times"></i>',
        //     },
        // }),


    ])




    function templateMain() {





        return `
        <div>
  <div class="image_info">
  <img src="https://media.istockphoto.com/photos/millennial-male-team-leader-organize-virtual-workshop-with-employees-picture-id1300972574?b=1&k=20&m=1300972574&s=170667a&w=0&h=2nBGC7tr0kWIU8zRQ3dMg-C5JLo9H2sNUuDjQ5mlYfo="  alt="" width="58px" height="58px">
  <div class="basic_info">
      <span >
          <span style="margin-right:8px;">  {{#helpers.highlight}}{ "attribute": "full_name" }{{/helpers.highlight}} </span>
           <span style="padding-left:8px;border-left: 1px solid grey;color: rgba(128, 128, 128, 0.707);">
           {{id}}  
           </span>
      </span>
          <div class="location_name">
          <i class="fas fa-map-marker-alt" style = "margin-right:5px" ></i> <span> {{location}}</span>
          </div>
  </div>
</div>
<div class="subs_info">
  <div class="social_acc_2">
          <img src="{{location}}" alt="">
          <span style="font-size: 16px;">
          25K</span>
  </div>
</div>


<div class="info_card_tags">
  <div class="main_tag" style="height: 50px;overflow: scroll;">
      <span>
         {{bio}}
      </span>
  </div>
  <div class="hastag_main" id="hashtags">
      
          #{{username}}
      
  </div>
</div>

<div class="add_to_list">
      
<div class='content'>


<button onClick="modalOpen('{{full_name}}',{{id}})" class='modal-toggle btn_modal'>
<a target = "_blank" href="addinfluencertolist/{{id}}">Add to list +</a></button>


</div>                
</div>

</div>
  `
    }


    search_one.start();
}





update();