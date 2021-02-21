$(document).ready(function(){
  /*
   * Materialise components initialisation
   */
  $('.sidenav').sidenav();
  $('.dropdown-trigger').dropdown({
    //Prevents the dropdown menu covering the trigger item
    coverTrigger: false
  });
  $('.collapsible').collapsible();
  $('.tabs').tabs();
});

/*
 * Submits ratings for recipes via AJAX
 */
//Binds AJAX handler to form submit event
$( "#recipe_rating_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, ratingSuccess);
});

//Binds star rating change event to trigger form submission
$( ".star-rating-ctl input[type=radio]" ).change(function() {
  console.log("triggering submit!")
  $( "#recipe_rating_form" ).submit();
});

function ratingSuccess(response) {
  console.log(response);
}

/*
 * Submits new comments for recipes via AJAX
 */
$( "#recipe_comment_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, commentSuccess);
});

function commentSuccess(response) {
  console.log(response);
}

/*
 * General function for submitting forms via AJAX
 */
function submitFormAJAX(event, callbackSuccess) {
  //Get form data
  var data = new FormData(event.target);
  var serialised = {};
  //serialise it into key/value pairs that can be converted to JSON
  for (var key of data.keys()) {
    serialised[key] = data.get(key);
  }
  //Make AJAX request
  $.ajax({
    type : "POST",
    url : $(event.target).attr("action"), //Get route from form action attribute
    contentType : 'application/json;charset=UTF-8',
    data : JSON.stringify(serialised),
    success : commentSuccess
  });
}
