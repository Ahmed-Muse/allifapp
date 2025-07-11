 

/*....this function is used for the select2 library....*/
    $(function () {
        $('.custom-field-class-for-seclect2').select2({
            placeholder: "Select The Correct Value Here",
            theme: "classic",
             width: '100%', // <--- CHANGE THIS TO '100%'
            //width: 'resolve', // 'resolve' is often better for responsive design
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
        if (openDropdown.classList.contains('allif-show') && openDropdown !== element.nextElementSibling) {
          openDropdown.classList.remove('allif-show');
        }
      }

      // Toggle the current dropdown
      element.nextElementSibling.classList.toggle("allif-show");
    }

    function confirmDelete(element) {
      const row = element.closest('tr');
  
      if (row) { // Check if row is not null
          if (currentConfirmRow && currentConfirmRow !== row) {
              if (currentConfirmRow.classList.contains("allif-confirm-delete-action")) {
                  currentConfirmRow.classList.remove("allif-confirm-delete-action");
              }
              const prevDropdown = currentConfirmRow.querySelector(".dropdown");
              const prevConfirm = currentConfirmRow.querySelector(".allif-confirm-action");
  
              if (prevDropdown) {
                  prevDropdown.style.display = "inline-block";
              }
              if (prevConfirm) {
                  prevConfirm.style.display = "none";
              }
          }
  
          row.classList.add("allif-confirm-delete-action");
  
          const rowDropDown = row.querySelector(".dropdown");
          const rowConfirm = row.querySelector(".allif-confirm-action");
          if (rowDropDown) {
              rowDropDown.style.display = "none";
          }
          if (rowConfirm) {
              rowConfirm.style.display = "inline-block";
          }
  
          currentConfirmRow = row;
      } else {
          console.error("Could not find table row for confirmation.");
      }
  }

    window.onclick = function(event) {
      if (!event.target.matches('.dropdown-content a') && !event.target.matches('.dropdown a')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
          var openDropdown = dropdowns[i];
          if (openDropdown.classList.contains('allif-show')) {
            openDropdown.classList.remove('allif-show');
          }
        }
      }
    }
 
////end...... this code is for opening the dropdown in the tables for delete inside the table///////


// below is for global search #######3 ... added on 1st July 2025....///

  $(document).ready(function() {
      const searchInput = $('#globalSearchInput');
      const searchResultsContainer = $('#globalSearchResults');
      const globalSearchModal = $('#globalSearchModal');

      // Use the globally defined variables
      const userVar = GLOBAL_USER_VAR;
      const glblSlug = GLOBAL_GLBL_SLUG;

      // Debugging check (will now show the values or empty strings if not passed from Django)
      console.log("User Var in JS:", userVar);
      console.log("Global Slug in JS:", glblSlug);

      let searchTimeout;

      // Clear search input and results when modal is hidden
      globalSearchModal.on('hidden.bs.modal', function () {
          searchInput.val('');
          searchResultsContainer.html('<p class="text-muted text-center">Start typing to find ERP features...</p>');
      });

      // Focus input when modal is shown
      globalSearchModal.on('shown.bs.modal', function () {
          searchInput.focus();
      });

      // Listen for input changes with debouncing
      searchInput.on('keyup', function() {
          const query = $(this).val().trim(); // Get trimmed query

          clearTimeout(searchTimeout); // Clear previous timeout

          if (query.length === 0) {
              searchResultsContainer.html('<p class="text-muted text-center">Start typing to find ERP features...</p>');
              return;
          }

          // Debounce the search request to avoid too many API calls
          searchTimeout = setTimeout(() => {
              performSearch(query);
          }, 300); // Wait 300ms after last keystroke
      });

      function performSearch(query) {
          // Check if slugs are valid before making API call
          if (!userVar || userVar === 'None' || !glblSlug || glblSlug === 'None') {
              searchResultsContainer.html('<p class="text-danger text-center">User or Company context missing. Cannot search.</p>');
              console.error("Cannot perform search: userVar or glblSlug is invalid.");
              return;
          }

          // Construct the API URL using the current user and company slugs
          const apiUrl = `/api/search-features/${userVar}/${glblSlug}/?q=${encodeURIComponent(query)}`;

          $.ajax({
              url: apiUrl,
              method: 'GET',
              success: function(data) {
                  searchResultsContainer.empty(); // Clear previous results

                  if (data.features && data.features.length > 0) {
                      data.features.forEach(feature => {
                          const resultItem = `
                              <a href="${feature.url}" class="list-group-item list-group-item-action search-result-item">
                                  <h5 class="mb-1">${feature.name} <small class="text-muted">(${feature.category})</small></h5>
                                  <p class="mb-1">${feature.description}</p>
                              </a>
                          `;
                          searchResultsContainer.append(resultItem);
                      });
                  } else {
                      searchResultsContainer.html('<p class="text-muted text-center">No features found matching your search.</p>');
                  }
              },
              error: function(xhr, status, error) {
                  console.error("Error searching features:", error);
                  searchResultsContainer.html('<p class="text-danger text-center">Error loading search results. Please try again.</p>');
              }
          });
      }
  });


    function sortTable(columnIndex) {
      const table = document.getElementById("sortable-table");
      const tbody = table.getElementsByTagName("tbody")[0];
      const rows = Array.from(tbody.rows);
      let sortDirection = table.getAttribute("data-sort-direction") || "asc";

      const compare = (rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].textContent.trim();
        const cellB = rowB.cells[columnIndex].textContent.trim();
        const dataTypeA = rowA.cells[columnIndex].dataset.type;
        const dataTypeB = rowB.cells[columnIndex].dataset.type;

        let valueA = cellA;
        let valueB = cellB;

        if (dataTypeA === "number" && dataTypeB === "number") {
          valueA = parseFloat(valueA);
          valueB = parseFloat(valueB);
        }

        if (sortDirection === "asc") {
          if (valueA < valueB) return -1;
          if (valueA > valueB) return 1;
          return 0;
        } else {
          if (valueA > valueB) return -1;
          if (valueA < valueB) return 1;
          return 0;
        }
      };

      rows.sort(compare);

      while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
      }

      rows.forEach(row => tbody.appendChild(row));

      table.setAttribute("data-sort-direction", sortDirection === "asc" ? "desc" : "asc");
    }

