$(document).ready(function(){
  /*
   * Materialise component initialisation
   */
  $('.sidenav').sidenav();
  $('.dropdown-trigger').dropdown({
    //Prevents the dropdown menu covering the trigger item
    coverTrigger: false
  });
  $('.timepicker').timepicker({
    twelveHour: false
  });
  $('.collapsible').collapsible();
  $('select').formSelect();
  $('.tabs').tabs();
});

$( "#steps" ).on("click", ".remove-list-item", function(event) {
  $( this ).parent().remove();
});
$( "#steps .add-list-item" ).click(function(event) {
  listItem =  "<li class='collection-item'>" +
                "<div class='input-field'>" +
                  "<textarea class='materialize-textarea' required>" +
                  "</textarea>" +
                "</div>" +
                "<a class='remove-list-item'><i class='material-icons'>clear</i></a>" +
              "</li>";
  $( this ).parent().before(listItem);
});

/*
 * Submits ratings for recipes via AJAX
 */
//Binds AJAX handler to form submit event
$( "#recipe_rating_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, ratingSuccess);

  //Stop reading star rating while server deals with request
  $( "input", this ).prop('disabled', true);
  $( ".star-rating-ctl", this ).addClass('disabled')
  //Show spinner to indicate users request is being dealt with
  $( ".preloader-wrapper", this ).removeClass("hide");
});

//Binds star rating change event to trigger form submission
$( ".star-rating-ctl input[type=radio]" ).change(function() {
  $( "#recipe_rating_form" ).submit();
});

function ratingSuccess(response) {
  //Stop reading star rating while server deals with request
  $( "input", "#recipe_rating_form" ).prop('disabled', false);
  $( ".star-rating-ctl", "#recipe_rating_form" ).removeClass('disabled')
  //Show spinner to indicate users request is being dealt with
  $( ".preloader-wrapper", "#recipe_rating_form" ).addClass("hide");
  //TODO: Update rating display element
}

/*
 * Submits new comments for recipes via AJAX
 */
$( "#recipe_comment_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, commentSuccess);

  /*Make the form read only so we don't spam the server before it's
    finished dealing with the current request.*/
  $( "input,textarea,button", this ).prop('readonly', true);
  $( "button", this ).prop('disabled', true);
  //Show spinner to indicate user's request is being dealt with
  $( ".preloader-wrapper", this ).removeClass('hide');
});

function commentSuccess(response) {
  //Reenable form and clear it's contents
  $( "input,textarea","#recipe_comment_form" ).prop('readonly', false);
  $( "button", "#recipe_comment_form").prop('disabled', false);
  $( "#recipe_comment_form" ).trigger("reset");
  //Hide the spinner
  $( "#recipe_comment_form .preloader-wrapper" ).addClass("hide");

  //Show the new comment at the top of the comment list
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
    success : callbackSuccess
  });
}
