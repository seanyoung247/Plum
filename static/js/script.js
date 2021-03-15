$(document).ready(function(){
  /*
   * Materialise component initialisation
   */
  $('.sidenav').sidenav();
  $('.dropdown-trigger').dropdown({
    // Prevents the dropdown menu covering the trigger item
    coverTrigger: false
  });
  $('.timepicker').timepicker({
    twelveHour: false
  });
  $('.collapsible').collapsible();
  $('select').formSelect();
});

/*
 * Closes flash messages
 */
$( ".flash-message-list" ).on("click", ".flash-close", function(event) {
  $( this ).closest( ".flash-message" ).remove();
});

/*
 * Adds a flash message as a response to an AJAX request
 */
function ajaxFlashResponse(response) {
  flashIcon = ( (response.category === "success") ? "check_circle" : response.category );
  flashMessage =
  `<li class="row flash-message ${response.category}">
    <div class="flash-icon">
      <i class="material-icons">${flashIcon}</i>
    </div>
    <div class="flash-content">
      ${response.message}
    </div>
    <a class="flash-close"><i class="material-icons">close</i></a>
  </li>`

  $( ".flash-message-list" ).append(flashMessage);
}

/*
 * Search Page
 */
$( "#advanced_search_toggle a" ).click(function(event) {
  $( "#advanced_search_pane" ).toggleClass("show").toggleClass("allow-overflow");
});

/*
 * General function for submitting forms via AJAX
 */
function submitFormAJAX(event, callbackSuccess) {
  // Get form data
  var data = new FormData(event.target);
  var serialised = {};
  // serialise it into key/value pairs that can be converted to JSON
  for (var key of data.keys()) {
    serialised[key] = data.get(key);
  }
  // Make AJAX request
  $.ajax({
    type : "POST",
    url : $(event.target).prop("action"), // Get route from form action attribute
    contentType : 'application/json;charset=UTF-8',
    data : JSON.stringify(serialised),
    success : callbackSuccess
  });
}
