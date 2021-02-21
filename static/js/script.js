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
  * Submits new comments and ratings for recipes via AJAX
  */
$( "#recipe_comment_form" ).submit(function(event) {
  event.preventDefault();

  //Get form data and serializes it
  var data = new FormData(this);
  var serialised = {};
  for (var key of data.keys()) {
    serialised[key] = data.get(key);
  }

  $.ajax({
    type : "POST",
    url : $(this).attr("action"),
    contentType : 'application/json;charset=UTF-8',
    data : JSON.stringify(serialised),
    success : commentSuccess
  });

  return false;
});

function commentSuccess(response) {
  console.log(response);
}
