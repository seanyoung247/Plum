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
  $('.fixed-action-btn').floatingActionButton({
    direction: 'bottom',
    hoverEnabled: false
  });
  $('.collapsible').collapsible();
  $('select').formSelect();
  $('.tabs').tabs();
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
                      <textarea name='steps' class='materialize-textarea' required>
                      </textarea>
                    </div>
                    <a class='remove-list-item'><i class='material-icons'>clear</i></a>
                  </li>`;
  $( this ).parent().before(listItem);
});
//Shows the current selected image in the image box
$( "#recipe_image" ).on('change', function(event){
  $( '#recipe_header_image' ).attr("src", $( this ).val())
});

// Shows the current selected image in the image box
$( "#recipe_image" ).on('change', function(event){
  $( '#recipe_header_image' ).prop("src", $( this ).val());
});

/*
 * Submits ratings for recipes via AJAX
 */
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

function ratingSuccess(response) {
  // Stop reading star rating while server deals with request
  $( "input", "#recipe_rating_form" ).prop('disabled', false);
  $( ".star-rating-ctl", "#recipe_rating_form" ).removeClass('disabled')
  // Show spinner to indicate users request is being dealt with
  $( ".preloader-wrapper", "#recipe_rating_form" ).addClass("hide");
  //TODO: Update rating display element
}

/*
 * Recipe favoriting
 */
$( "#recipe_favorite_form" ).submit(function(event) {
  event.preventDefault();
  // There's no real need for a callback here
  submitFormAJAX(event, null);
});

$( "#recipe_favorite input[type=checkbox]" ).on('change', function(event) {
  $( '#recipe_favorite_form' ).submit();
});

/*
 * Submits new comments for recipes via AJAX
 */
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
                          <p>${response.author.name}</p>
                          <p>${response.text}</p>
                        </div>
                      </div>`;
  $( "#recipe_comments_wrapper" ).prepend(commentHTML);
}

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

/*
 * Horizontal scroller component
 */
// Scrolls one "page" left (backwards)
$( ".scroller .scroll-left" ).click(function(event) {
  let scroller = $( this ).siblings(".scroller-items");
  let scrollItem = scroller.children(".scroll-item");
  // Next page position = current page position - items in a page (scroll backwards)
  let itemPosition = parseInt(scroller.attr("data-position"))
  // If we're at the beginning of the list wrap around to the end
  if (itemPosition <= 0) itemPosition = scrollItem.length;
  else itemPosition -= Math.floor(scroller.outerWidth() / scrollItem.outerWidth());
  // Update data position so we know where we are in the list
  scroller.attr("data-position", itemPosition);
  // Animate the scroll
  scroller.animate({scrollLeft: (itemPosition * scrollItem.outerWidth())}, 500);
});

// Scrolls one "page" right (forwards)
$( ".scroller .scroll-right" ).click(function(event) {
  let scroller = $( this ).siblings(".scroller-items");
  let scrollItem = scroller.children(".scroll-item");
  // Next page position = current page position + items in a page (scroll forwards)
  let itemPosition = parseInt(scroller.attr("data-position")) +
    Math.floor(scroller.outerWidth() / scrollItem.outerWidth());
  // If we're at the end of the list wrap around to the beginning
  if (itemPosition >= scrollItem.length) itemPosition = 0;
  // Update data position so we know where we are in the list
  scroller.attr("data-position", itemPosition);
  // Animate the scroll
  scroller.animate({scrollLeft: (itemPosition * scrollItem.outerWidth())}, 500);
});

// Updates scroller position when scrolling has finished
$( ".scroller .scroller-items" ).scroll(function() {
  clearTimeout($(this).data("scroller-scrollTimer"));
  console.log("test");
  // Scroll event has ended
  $( this ).data("scroller-scrollTimer", setTimeout(() => {
    // Get the first full item shown in the scroller
    itemPosition = Math.round($( this ).scrollLeft() /
      $( this ).children(".scroll-item").outerWidth());
    // Update the scroll position
    $( this ).attr("data-position", itemPosition);
  }, 250));
});
