

// function closeMenu() {  
//     var menu = document.getElementById("menu_box")
//     var closeBtn = document.getElementById("btn_close")
//     menu.setAttribute('style','display:none')
//     closeBtn.setAttribute('style', 'visibility:hidden')

    
//    }

//    function openMenu(){
//     var menu = document.getElementById("menu_box")
//     var closeBtn = document.getElementById("btn_close")
//     menu.setAttribute('style','visibility:visible')
//     closeBtn.setAttribute('style', 'visibility:visible')
//    }



// NEW JS




// Global variables
var menu = document.getElementById("menu_box")
var closeBtn = document.getElementById("btn_close")
var tabs = document.querySelectorAll('[data-set-tab]')
var tabContents = document.querySelectorAll('[data-set-target]')
var socialContent = document.getElementById('social_icons_new')


// --------Profile Tabs Variables
var profileTags= document.querySelectorAll("[data-profile-btn]")
var profileContents = document.querySelectorAll('[data-profile-target]')


// Profile select buttons

// var profileButtons = document.querySelectorAll('[data-btn-tags')






// 

function closeMenu() {  
    menu.setAttribute('style','display:none')
    closeBtn.setAttribute('style', 'visibility:hidden')
   }

   function openMenu(){

    menu.setAttribute('style','visibility:visible')
    closeBtn.setAttribute('style', 'visibility:visible')
   }

 
tabs.forEach(function(tab){
    tab.addEventListener('click' , function(){
        
        const target = document.querySelector(tab.dataset.setTab)
            if(target.id == "dashboard"){
               socialContent.classList.remove('not_active_social') 
            }
            else{
                socialContent.classList.add('not_active_social')
                console.log("not_active");
            }


        tabContents.forEach(function(tabContent){
            tabContent.classList.remove('active')
        })
        tabs.forEach(function(tab){
            tab.classList.remove('active')
        })
        tab.classList.add('active')

        target.classList.add('active')
        closeMenu()
    })
})



const btnsTip = document.querySelectorAll("[data-btn-tags]");
let activeBtn = null;
var count = 0
btnsTip.forEach((btnTip) => {
  btnTip.addEventListener("click", (e) => {
      count+=1
    e.currentTarget.classList.add("tag_active");
    activeBtn = e.currentTarget;
    if(count>5){
        alert("5 slected")
    }
    else if ((activeBtn = null && activeBtn != e.currentTarget)) {  
        activeBtn.classList.remove("tag_active");
      } 
  });
});


profileTags.forEach(function(tag){
    tag.addEventListener('click', function(){
        let targetTab = document.querySelector(tag.dataset.profileBtn)
        profileContents.forEach(function(profileContent){
            profileContent.classList.remove('active')
            profileTags.forEach(function(tag){
                tag.classList.remove('active_color')
            })
            tag.classList.add('active_color')
        })
        targetTab.classList.add('active')
    })
})



// Profile and user buttons switch in profile section

const switchProfiles = document.querySelectorAll('[data-profile-tabs]')
const switchTabs = document.querySelectorAll('[data-main-profiles]')
const btnProfile = document.getElementById("profile_heading_1")
const btnProfileTwo = document.getElementById("profile_heading_2")
const profileSideList = document.getElementById("profile_side_list")
const usersSideList = document.getElementById("users_side_list")


switchProfiles.forEach(function(event){
    let targetTab = document.querySelector(event.dataset.profileTabs)
    event.addEventListener('click' , function(){
        switchTabs.forEach(function(tab){
            tab.classList.remove('profile_main_active')
            

            if(targetTab.id === 'container_user'){
                btnProfile.classList.add('heading_none')
                btnProfileTwo.classList.remove("heading_none")
                btnProfileTwo.innerHTML = "User"
                usersSideList.classList.remove("display_none")
                profileSideList.classList.add("display_none")

            }
            else{
                btnProfileTwo.classList.add("heading_none")
                btnProfile.classList.remove("heading_none")
                usersSideList.classList.add("display_none")
                profileSideList.classList.remove("display_none")

            }

            switchProfiles.forEach(function(tab){
                tab.classList.remove('btn_profile_color')
            })
            event.classList.add('btn_profile_color')
            

        })
        targetTab.classList.add('profile_main_active')
    })
})




// Profile and user side menu
const userButtonTabs = document.querySelectorAll('[data-user-btn]')
const userButtonTarget = document.querySelectorAll('[data-user-targetMain]')

userButtonTabs.forEach(function(usertab){
    let targetTab = document.querySelector(usertab.dataset.userBtn)
    usertab.addEventListener('click', function(){
        userButtonTarget.forEach(function(btnTarget){
            btnTarget.classList.remove('display_block')
            userButtonTabs.forEach(function(btn){
                btn.classList.remove('active_color')
            })
            usertab.classList.add("active_color")
        })
       targetTab.classList.add("display_block") 
    })
})



document.getElementById('user_form').addEventListener('click',function(e){
   
    let bio = document.forms["profile_form"]["bio"].value

    console.log(bio.length);




})


// var searchInput = 'search_input'
// console.log("input");

// $(document).ready(function(){
//     var autocomplete;
//     autocomplete = new.google.maps.places.Autocomplete((document.getElementById(searchInput)),{
//         types:["geocode"]
//     });
//     google.maps.event.addEventListener(autocomplete, 'place_changed',function(){
//         var near_place = autocomplete.getPlace();
//         console.log(near_place);
//     })
// })

