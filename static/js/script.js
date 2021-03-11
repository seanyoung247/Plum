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
  $('select').formSelect();
});

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

/*
 * Horizontal scroller component
 */
// Scrolls one "page" left (backwards)
$( ".scroller .scroll-left" ).click(function(event) {
  let scroller = $( this ).siblings( ".scroller-items" );
  let scrollItem = scroller.children( ".scroll-item" );
  let scrollEndItem = scroller.children( ".scroll-item-bookend" );
  let scrollPosition = scroller.get(0).scrollWidth;
  // If we're at the beginning of the items, move back one page
  if (scroller.scrollLeft() > 0) {
    // Which item is left most?
    let leftMostItem = Math.ceil((scroller.scrollLeft()) / scrollItem.outerWidth());
    // How many items fit in a page?
    let pageItemWidth = Math.floor(scroller.width() / scrollItem.outerWidth());
    // Calculate new scroll position: Find out which item should be left most
    //  then calulate it's position by multiplying it by icon width
    scrollPosition = ((leftMostItem - pageItemWidth) * scrollItem.outerWidth());
  }
  scroller.animate({scrollLeft: scrollPosition}, 500);
});

// Scrolls one "page" right (forwards)
$( ".scroller .scroll-right" ).click(function(event) {
  let scroller = $( this ).siblings( ".scroller-items" );
  let scrollItemWidth = scroller.children( ".scroll-item" ).outerWidth();
  let scrollEndPosition = scroller.scrollLeft() + scroller.width() +
    scroller.children( ".scroll-item-bookend" ).outerWidth();
  let scrollPosition = 0;
  // If we're not at the end of the items move to the next page
  if (scrollEndPosition < (scroller.get(0).scrollWidth - 1)) {
    // Which item is left most?
    let leftMostItem = Math.floor((scroller.scrollLeft()) / scrollItemWidth);
    // How many items fit in a page?
    let pageItemWidth = Math.floor(scroller.width() / scrollItemWidth);
    // Calculate new scroll position: Find out which item should be left most
    //  then calulate it's position by multiplying it by icon width
    scrollPosition = ((leftMostItem + pageItemWidth) * scrollItemWidth);
  }
  scroller.animate({scrollLeft: scrollPosition}, 500);
});
