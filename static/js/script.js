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
  var formData = $(this).serializeArray();

  var test = {
    "recipeId": formData[0].value,
    "rating": formData[1].value,
    "comment": formData[2].value
  };

  $.ajax({
    type : "POST",
    url : $(this).attr("action"),
    contentType : 'application/json;charset=UTF-8',
    data : JSON.stringify(test)
  });
});
