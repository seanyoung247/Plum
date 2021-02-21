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

  //Make the form read only so we don't spam the server before it's
  $( "input,textarea,button",this ).prop('readonly', true);
  $( "button",this ).prop('disabled', true);
  //Show spinner to indicate user's request is being
  $( ".preloader-wrapper",this ).removeClass("hide");
});

function commentSuccess(response) {
  //Reenable form and clear it's contents
  $( "input,textarea","#recipe_comment_form" ).prop('readonly', false);
  $( "button", "#recipe_comment_form").prop('disabled', false);
  $( "#recipe_comment_form" ).trigger("reset");
  //Show spinner to indicate user's request is being
  $( "#recipe_comment_form .preloader-wrapper" ).addClass("hide");

  //Show the new comment at the top of the list
  commentHTML = "<div class='row'><div class='col s12'><p>"
    + response.author.name + "</p><p>" + response.text + "</p></div></div>";
    $( "#recipe-comments-wrapper" ).prepend(commentHTML);
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
