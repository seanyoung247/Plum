$(document).ready(function() {
  $('.tabs').tabs();
  $('.modal').modal();
});

// Binds AJAX handler to form submit event
$( "#recipe_rating_form" ).submit(function(event) {
  event.preventDefault();

  submitFormAJAX(event, ratingSuccess);
  // Stop reading star rating while server deals with request
  $( "input", this ).prop('disabled', true);
  $( ".star-rating-ctl", this ).addClass('disabled');
  // Show spinner to indicate users request is being dealt with
  $( ".preloader-wrapper", this ).removeClass("hide");
});

// Log that the rating value has changed.
$( ".star-rating-ctl input[type='radio']" ).change(function(event) {
  $( ".star-rating-ctl" ).prop("data-rating-changed", true);
});

// Submits the rating form only when losing focus and value has changed
$( ".star-rating-ctl" ).focusout(function(event) {
  /* If the new focus item isn't a child of the star-rating-ctl radio-group,
     focus has left the button group (and not just an individual radio button). */
  if (this != $( event.relatedTarget ).parent()[0] ) {
    // Only submit if the value has actually been changed
    if ($( this ).prop("data-rating-changed")) {
      $( this ).prop("data-rating-changed", false);
      $( "#recipe_rating_form" ).submit();
    }
  }
});

// Called if setting the rating was successful
function ratingSuccess(response) {
  // Stop reading star rating while server deals with request
  $( "input", "#recipe_rating_form" ).prop('disabled', false);
  $( ".star-rating-ctl", "#recipe_rating_form" ).removeClass('disabled');
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
$( "#recipe_favorite input[type=checkbox]" ).change(function(event) {
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
  let commentHTML =
    `<div class="comment-wrapper">
        <div class="comment-author">
          <a href="${response.response.profile}">${response.response.author}</a>
        </div>
        <div class="comment-box">
          <p class="comment-content">${response.response.text}</p>
          <a class="delete-comment btn-floating btn-small btn-plum">
            <i class="material-icons">delete_outline</i>
          </a>
        </div>
      </div>`;

  $( "#recipe_comments_wrapper" ).append(commentHTML);
}

$( "#recipe_comments_wrapper" ).on("click", ".delete-comment", function(event) {

  data = {
    "recipe" : $( "#recipeId" ).val(),
    "comment" : $( this ).closest(".comment-wrapper").index()
  }

  $( this ).closest(".comment-wrapper").remove();
  $.ajax({
    type : "POST",
    url : $( "#recipe_comments_wrapper" ).attr("data-delete-comment"),
    contentType : 'application/json;charset=UTF-8',
    data : JSON.stringify(data),
    success : ajaxFlashResponse
  });
});

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
                      <input name='ingredients' type='text' maxlength='100' required>
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
$( "#recipe_image_url" ).on('change', function(event) {
  $( '#recipe_header_image' ).prop("src", $( this ).val());
});

// cloudinary callback. Sets upload image url input
function imageUploaded(error, result) {
  $( '#recipe_header_image' ).prop("src", result[0].secure_url);
  $( '#recipe_image_url' ).val(result[0].secure_url);
}

// Shows the cloudinary image upload widget
$( "#image_upload_btn" ).click(function(event) {
  event.preventDefault();

  cloudinary.openUploadWidget(
    {
      cloud_name: 'dtx8mohkg',
      upload_preset: 'plum8hdx'
    },
    imageUploaded);
});
