$(document).ready(function(){
  $('.sidenav').sidenav();
  $(".dropdown-trigger").dropdown({
    //Prevents the dropdown menu covering the trigger item
    coverTrigger: false
  });
  $('.collapsible').collapsible();
  $('.tabs').tabs();
});
