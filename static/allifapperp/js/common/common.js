 

/*....this function is used for the select2 library....*/
    $(function () {
        $('.custom-field-class-for-seclect2').select2({
            placeholder: "Select The Correct Value Here",
            theme: "classic",
            width: 'resolve', // 'resolve' is often better for responsive design
            closeOnSelect: true,
            disabled: false,
            dropdownCssClass: "form-control", // Use dropdownCssClass instead of customClass
        });
    });


//<!-- start --below is for turning the color of the clicked row-->
$(function() {
    //Highlight clicked row
    $('.table-layout td').on('click', function() {
    
      // Remove previous highlight class
      $(this).closest('table').find('tr.clickedrow').removeClass('clickedrow');
      
      // add highlight to the parent tr of the clicked td...eval
      $(this).parent('tr').addClass("clickedrow");
    });
    });
    

    
    ////start...... this code is for opening the dropdown in the tables for delete inside the table///////
   
    let currentConfirmRow = null;

    function showDropdown(event, element) {
      event.preventDefault();

      // Close other open dropdowns
      var dropdowns = document.getElementsByClassName("dropdown-content");
      for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show') && openDropdown !== element.nextElementSibling) {
          openDropdown.classList.remove('show');
        }
      }

      // Toggle the current dropdown
      element.nextElementSibling.classList.toggle("show");
    }

    function confirmDelete(element) {
      const row = element.closest('tr'); // Get the closest <tr> element

      if (currentConfirmRow && currentConfirmRow !== row) {
        currentConfirmRow.classList.remove("confirm-delete");
        currentConfirmRow.querySelector(".dropdown").style.display = "inline-block";
        currentConfirmRow.querySelector(".confirm-delete-dropdown").style.display = "none";
      }

      row.classList.add("confirm-delete");
      row.querySelector(".dropdown").style.display = "none";
      row.querySelector(".confirm-delete-dropdown").style.display = "inline-block";

      currentConfirmRow = row;
    }

    window.onclick = function(event) {
      if (!event.target.matches('.dropdown-content a') && !event.target.matches('.dropdown a')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
          }
        }
      }
    }
 
////end...... this code is for opening the dropdown in the tables for delete inside the table///////

