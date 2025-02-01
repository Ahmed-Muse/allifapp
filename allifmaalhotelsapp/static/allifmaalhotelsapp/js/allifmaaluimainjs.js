

  
    /* Toggle between adding and removing the responsive "opentonavhiddenlinks" class to
     allifmaaltopnavone top navigation bar when the user clicks on the icon classed as allifmaaltopnavoneicon */

     /*############################### START....TOP NAVIGATION BARS SECTION ...#########################3*/
  function opentopnavonehiddenlinks() {
    var x = document.getElementById("allifmaaltopnavoneid");
    if (x.className === "allifmaaltopnavone") {
      x.className += " opentopnavhiddenlinks";//dont remove space..if you remove, the class will not be applied when 
      //you open the closed links... this makes the top navigation bar responsive to various screen sizes.
      //Having no space between .topnav and .opentonavhiddenlinks means it will select an element with 
      //both class names. If you add the space in between, you would be selected all (if any)
      // element having the opentonavhiddenlinks class name with a 
      //parent (or grandparent, or grand-grand-...-parent) having a allifmaaltopnavone class name..eval.
    } else {
      x.className = "allifmaaltopnavone";
    }
  }
  //Basically, javascript:void(0); means "do nothing". The javascript: part means the 
  //following part is coded in javascript and the void(0) is a statement that does 
  //nothing and returns undefined, in javascript.
  //The line x.className += " opentonavhiddenlinks"; adds the opentonavhiddenlinks class name to the x element.
  // If x had the class name allifmaaltopnavone, after this line it will have both class names, matching 
  //the .allifmaaltopnavone.opentonavhiddenlinks CSS selector.

    /* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
    /*show the links in the drop down buttons*/
    var topnavonedropdownbtns= document.getElementsByClassName("topnavonedropdownbtn");
    var i;
    for (i = 0; i < topnavonedropdownbtns.length; i++) {
      topnavonedropdownbtns[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var topnavonedropdownbtnlinks = this.nextElementSibling;
        if (topnavonedropdownbtnlinks.style.display === "block") {
          topnavonedropdownbtnlinks.style.display = "none";
        } else {
          topnavonedropdownbtnlinks.style.display = "block";
        }
      });
    }
    

    //open top nav menu topnavmenudropdownmenu
  $(document).ready(function(){
  $(".opentopnavdropdownmenulinkone").click(function(){
    /*get the button with class name opentopnavdropdownmenulink and then switch between two classes below*/
  $(".topnavmenudropdownmenuonewithclose").toggleClass( "showhiddentopnavmenuwindowwithclose" );
  })
  })

  //open top nav menu topnavmenudropdownmenu
  $(document).ready(function(){
  $(".opentopnavdropdownmenulinktwo").click(function(){
    /*get the button with class name opentopnavdropdownmenulink and then switch between two classes below*/
  $(".topnavmenudropdownmenutwowithclose").toggleClass( "showhiddentopnavmenuwindowwithclose" );
  })
  })

  //open top nav menu topnavmenudropdownmenu
  $(document).ready(function(){
    $(".opentopnavdropdownmenulinkthree").click(function(){
      /*get the button with class name opentopnavdropdownmenulink and then switch between two classes below*/
    $(".topnavmenudropdownmenuthreewithclose").toggleClass( "showhiddentopnavmenuwindowwithclose" );
    })
    })
    /*.....end.........top navigation bare drop down opening function...*/


/*############################### START....SIDE NAVIGATION BARS SECTION ...#########################3*/
  // function to open side nav bar menu one when hidden....opensidenavone
  $(document).ready(function(){
$(".opensidemenuonebtn").click(function(){
$(".sidenavonemenu").toggleClass( "opensidenavone" );
})
})

// function to open side nav bar menu two when hidden....opensidenavtwo
    $(document).ready(function(){
  $(".opensidemenutwobtn").click(function(){
  $(".sidenavtwomenu").toggleClass( "opensidenavtwo" );
  })
  })

  // function to open side nav bar menu three when hidden....opensidenavthree
  $(document).ready(function(){
  $(".opensidemenuthreebtn").click(function(){
  $(".sidenavthreemenu").toggleClass( "opensidenavthree" );
  })
  })
  
  /*open hidden links in the drop down sections of the side nav bars.....*/
    /* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
    /*show the links in the drop down buttons*/
    var sidenavonedropdownbtns= document.getElementsByClassName("sidenavonedropdownbtn");
    var i;
    for (i = 0; i < sidenavonedropdownbtns.length; i++) {
      sidenavonedropdownbtns[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var sidenavonedropdownbtnlinks = this.nextElementSibling;
        if (sidenavonedropdownbtnlinks.style.display === "block") {
          sidenavonedropdownbtnlinks.style.display = "none";
        } else {
          sidenavonedropdownbtnlinks.style.display = "block";
        }
      });
    }
   
    
    var sidenavtwodropdownbtns= document.getElementsByClassName("sidenavtwomenudropdownbtn");
    var i;
    for (i = 0; i < sidenavtwodropdownbtns.length; i++) {
      sidenavtwodropdownbtns[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var sidenavtwodropdownbtnlinks= this.nextElementSibling;
        if (sidenavtwodropdownbtnlinks.style.display === "block") {
          sidenavtwodropdownbtnlinks.style.display = "none";
        } else {
          sidenavtwodropdownbtnlinks.style.display = "block";
        }
      });
    }
    

    var sidenavtwodropdownbtns= document.getElementsByClassName("sidenavthreemenudropdownbtn");
    var i;
    for (i = 0; i < sidenavtwodropdownbtns.length; i++) {
      sidenavtwodropdownbtns[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var sidenavtwodropdownbtnlinks= this.nextElementSibling;
        if (sidenavtwodropdownbtnlinks.style.display === "block") {
          sidenavtwodropdownbtnlinks.style.display = "none";
        } else {
          sidenavtwodropdownbtnlinks.style.display = "block";
        }
      });
    }
    

    //////////////////////////////// BELOW IS FOR BODY /////////////////////////

  /* .... Start.....Module menus ..... containing hidden module links...... */

  /* .... Menu one...... */
  $(document).ready(function(){
$(".module-menu-one-open-link").click(function(){
$(".module-menu-one").toggleClass("module-menu-window");
})
})

/* .... Menu two...... */
$(document).ready(function(){
$(".module-menu-two-open-link").click(function(){
$(".module-menu-two").toggleClass("module-menu-window");
})
})

/* .... Menu two...... */
$(document).ready(function(){
$(".module-menu-three-open-link").click(function(){
$(".module-menu-three").toggleClass("module-menu-window");
})
})


/* .... Module drop down container section..... containing hidden module links...... */
var sidenavtwodropdownbtns= document.getElementsByClassName("module-menu-dropdown-btn");
    var i;
    for (i = 0; i < sidenavtwodropdownbtns.length; i++) {
      sidenavtwodropdownbtns[i].addEventListener("click", function() {
        var sidenavtwodropdownbtnlinks= this.nextElementSibling;
        if (sidenavtwodropdownbtnlinks.style.display === "block") {
          sidenavtwodropdownbtnlinks.style.display = "none";
        } else {
          sidenavtwodropdownbtnlinks.style.display = "block";
        }
      });
    }
    /* .... Start.....Module menu one ..... containing hidden module links...... */
    /* .... End.....Module menu one ..... containing hidden module links...... */
  


 
//<!-- start --below is for turning the color of the clicked row-->
  $(document).ready(function() {

//Highlight clicked row
$('.table-layout td').on('click', function() {

  // Remove previous highlight class
  $(this).closest('table').find('tr.clickedrow').removeClass('clickedrow');
  
  // add highlight to the parent tr of the clicked td...eval
  $(this).parent('tr').addClass("clickedrow");
});
});

//<!-- end --below is for turning the color of the clicked row-->

/* When the user clicks on the button...toggle between hiding and showing the dropdown content */
function openModuleMenuOne() {
  document.getElementById("content-dropdown-menu-one-id").classList.toggle("module-dropdown-menu");
    }
    
  /* When the user clicks on the button....toggle between hiding and showing the dropdown content */
function openModuleMenuTwo() {
  document.getElementById("content-dropdown-menu-two-id").classList.toggle("module-dropdown-menu");
  }
  
  /* When the user clicks on the button...toggle between hiding and showing the dropdown content */
function openModuleMenuThree() {
  document.getElementById("content-dropdown-menu-three-id").classList.toggle("module-dropdown-menu");
  }



  
 
  
    
    



   