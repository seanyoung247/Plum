$(document).ready(function(){
  $('.sidenav').sidenav();
  $(".dropdown-trigger").dropdown({
    coverTrigger: false
  });

  $('.collapsible').collapsible(); //Might be better to be inserted on the page?
});
