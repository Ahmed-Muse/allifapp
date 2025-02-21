 

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
    
