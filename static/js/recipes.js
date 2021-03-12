$(document).ready(function() {
  $('.tabs').tabs();
});

// Binds AJAX handler to form submit event
$( "#recipe_rating_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, ratingSuccess);

  // Stop reading star rating while server deals with request
  $( "input", this ).prop('disabled', true);
  $( ".star-rating-ctl", this ).addClass('disabled')
  // Show spinner to indicate users request is being dealt with
  $( ".preloader-wrapper", this ).removeClass("hide");
});

// Binds star rating change event to trigger form submission
$( ".star-rating-ctl input[type=radio]" ).change(function() {
  $( "#recipe_rating_form" ).submit();
});

// Called if setting the rating was successful
function ratingSuccess(response) {
  // Stop reading star rating while server deals with request
  $( "input", "#recipe_rating_form" ).prop('disabled', false);
  $( ".star-rating-ctl", "#recipe_rating_form" ).removeClass('disabled')
  // Show spinner to indicate users request is being dealt with
  $( ".preloader-wrapper", "#recipe_rating_form" ).addClass("hide");
  //TODO: Update rating display element
}

// Submits the favorite to the server
$( "#recipe_favorite_form" ).submit(function(event) {
  event.preventDefault();
  // There's no real need for a callback here
  submitFormAJAX(event, null);
});

// Binds favorite form submit to the favorite control change event
$( "#recipe_favorite input[type=checkbox]" ).on('change', function(event) {
  $( '#recipe_favorite_form' ).submit();
});


// Submits a comment to the AJAX route
$( "#recipe_comment_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, commentSuccess);

  /* Make the form read only so we don't spam the server before it's
     finished dealing with the current request. */
  $( "input,textarea,button", this ).prop('readonly', true);
  $( "button", this ).prop('disabled', true);
  // Show spinner to indicate user's request is being dealt with
  $( ".preloader-wrapper", this ).removeClass('hide');
});

// Comment success callback
function commentSuccess(response) {
  // Reenable form and clear it's contents
  $( "input,textarea","#recipe_comment_form" ).prop('readonly', false);
  $( "button", "#recipe_comment_form").prop('disabled', false);
  $( "#recipe_comment_form" ).trigger("reset");
  // Hide the spinner
  $( "#recipe_comment_form .preloader-wrapper" ).addClass("hide");

  // Show the new comment at the top of the comment list
  let commentHTML =  `<div class='row'>
                        <div class='col s12'>
                          <p>${response.author}</p>
                          <p>${response.text}</p>
                        </div>
                      </div>`;
  $( "#recipe_comments_wrapper" ).prepend(commentHTML);
}
/*
 * Edit/Add Recipe page
 */
// Removes a list item from the method or ingredients lists
$( "#steps, #ingredients").on("click", ".remove-list-item", function(event) {
  $( this ).parent().remove();
});

// Adds a list item to the ingredients list
$( "#ingredients .add-list-item" ).click(function(event) {
  let listItem = `<li class='collection-item'>
                    <div class='input-field'>
                      <input name='ingredients' type='text' required>
                    </div>
                    <a class='remove-list-item'><i class='material-icons'>clear</i></a>
                  </li>`;
  $( this ).parent().before(listItem);
});

// Adds a list item to the method list
$( "#steps .add-list-item" ).click(function(event) {
  let listItem =  `<li class='collection-item'>
                    <div class='input-field'>
                      <textarea name='steps' class='materialize-textarea' required></textarea>
                    </div>
                    <a class='remove-list-item'><i class='material-icons'>clear</i></a>
                  </li>`;
  $( this ).parent().before(listItem);
});

// Shows the current selected image in the image box
$( "#recipe_image" ).on('change', function(event){
  $( '#recipe_header_image' ).prop("src", $( this ).val())
});
