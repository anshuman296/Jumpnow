// Feather icon Set

feather.replace()


// Feather icon






const leftButtons = document.querySelectorAll('[data-btn-left')
const openMenu = document.getElementById('ham_menu')
const leftMenu = document.getElementById('left')
const closeMenu = document.getElementById('btn_close')
var tabContents = document.querySelectorAll('[data-set-target]')




// Button Logic
openMenu.addEventListener("click", function() {
    leftMenu.classList.add("show")
    closeMenu.classList.add("show")

    closeMenu.addEventListener("click", function() {
        leftMenu.classList.remove("show")
        closeMenu.classList.remove("show")
    })

})


// Active Class on click

leftButtons.forEach(function(btn) {
    // let target = btn.target

    btn.addEventListener("click", function() {

        // const target = document.querySelector(btn.dataset.btnLeft)

        // if (target.id === "right_list") {
        //     closeFilter()

        // alert(location.href.split('/'))
        // window.location.href = window.location.origin + "discovery/showcampaignlists/"
        // }

        // tabContents.forEach(function(tabContent) {
        //     tabContent.classList.remove('active')
        // })

        leftButtons.forEach(function(btn) {
            btn.classList.remove("border_show")
        })
        btn.classList.add("border_show")
            // leftMenu.classList.remove("show")
            // closeMenu.classList.remove("show")

        // target.classList.add('active')

    })
})


// Pagination











// Filter and Sort

const filterBtn = document.getElementById("filter")
const sortBtn = document.getElementById('sort')
const filtSortCont = document.getElementById('filter_sort')
const menuText = document.querySelectorAll("#left_menu_txt")
const logo_1 = document.getElementById("logo_1_jn")
const logo_2 = document.getElementById("logo_2_jn")
const leftMenuShrink = document.getElementById("left")

var count = 2

filterBtn.addEventListener("click", function() {
    if (count % 2 == 0) {
        console.log(count);

        menuText.forEach(function(txt) {
            txt.classList.add("hide")
        })
        logo_1.style.display = "none";
        logo_2.style.display = "block";
        leftMenuShrink.style.flex = ".3"
        document.getElementById("middle").style.display = "block"
        leftButtons.forEach(function(btn) {
            btn.classList.add("big_font")
        })
        filterBtn.style.border = "1px solid white"
        filterBtn.style.display = "none"



    } else {

        console.log("not Yahoo");
        menuText.forEach(function(txt) {
            txt.classList.remove("hide")
        })
        logo_1.style.display = "block";
        logo_2.style.display = "none";
        leftMenuShrink.style.flex = "1.3"
        document.getElementById("middle").style.display = "none"
        leftButtons.forEach(function(btn) {
            btn.classList.remove("big_font")
        })

    }


})





// document.getElementById('close_filter_menu').addEventListener("click", function() {
//     document.getElementById('middle').style.display = "none"

//     menuText.forEach(function(txt) {
//         txt.classList.remove("hide")
//     })
//     logo_1.style.display = "block";
//     logo_2.style.display = "none";
//     leftMenuShrink.style.flex = "1.3"
//     document.getElementById("middle").style.display = "none"
//     leftButtons.forEach(function(btn) {
//         btn.classList.remove("big_font")
//     })
//     filterBtn.style.display = "block"



//     count = 2;
// })


function closeFilter() {
    document.getElementById('middle').style.display = "none"

    menuText.forEach(function(txt) {
        txt.classList.remove("hide")
    })
    logo_1.style.display = "block";
    logo_2.style.display = "none";
    leftMenuShrink.style.flex = "1.3"
    document.getElementById("middle").style.display = "none"
    leftButtons.forEach(function(btn) {
        btn.classList.remove("big_font")
    })
    filterBtn.style.display = "block"



    count = 2;
}




// Search Input

const searchField = document.getElementById("search_icon")
const filterSort = document.getElementById("filter_sort")
    // const searchFieldSocial = document.getElementById("search_input")

// document.getElementById("search_input").addEventListener("keyup",function(event){
//     event.preventDefault
// })

const searchFields = document.querySelectorAll('[data-search-main]')


searchFields.forEach(function(search) {
    search.addEventListener("click", function(a) {
        filterSort.classList.add("show")
        document.getElementById("top").classList.add('hide')
        document.getElementById("heading_content").classList.add("hide")
        document.getElementById("search_bar").classList.add("rmv_margin")
        document.getElementById("card_container").classList.add("show")
            // logo_1.style.display = "block";
        logo_2.style.display = "none";

        contentWrapper.classList.remove('modal--active');
        modalWrapper.classList.remove('modal--active');

    })
})

// Search in showcampaignlist

function searchFun() {
    let filter_list = document.getElementById('myInput').value.toUpperCase()
    let myTable = document.getElementById('customers')
    let tr = myTable.getElementsByTagName('tr')

    for (var i = 0; i < tr.length; i++) {
        let td = tr[i].getElementsByTagName('td')[0]
        let td_socials = tr[i].getElementsByTagName('td')[1]
            // td = td.replace(/(\r\n|\n|\r)/gm, "");
            // td = td.replace(/\s+/g, ' ').trim()

        if (td) {
            let textValue = td.textContent || td.innerHTML
            let textValueTwo = td_socials.textContent || td_socials.innerHTML

            if (textValue.toUpperCase().indexOf(filter_list) > -1 || textValueTwo.toUpperCase().indexOf(filter_list) > -1) {
                tr[i].style.display = ""
            } else {
                tr[i].style.display = "none"
            }
        }
    }

}

// Sorting table

// Checking Length of table


// Left buttons navigations


// Show Campaign List create select custom