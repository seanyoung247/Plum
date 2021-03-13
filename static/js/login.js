$(document).ready(function() {
  $('.tabs').tabs();
});

// Sends an AJAX request to the server to check if username is available
$( "#register-username" ).focusout(function(event) {
  event.preventDefault();
  // Make AJAX request
  $.ajax({
    type : "POST",
    url : $(event.target).attr("data-validate"),
    contentType : 'application/json;charset=UTF-8',
    data : JSON.stringify({ "username" : $( this ).val() }),
    success : callBackUsername
  });
  return false;
});

function callBackUsername(response) {
  if ( response["exists"] ) {
    $( "#register-username" ).removeClass("valid").addClass("invalid");
    // Don't let the user submit the form if the username is taken
    $( "#register-username" )[0].setCustomValidity("Username already exists");
  } else {
    $( "#register-username" ).removeClass("invalid").addClass("valid");
    $( "#register-username" )[0].setCustomValidity("");
  }
}

// Checks if confirm password field matches password field and sets it valid/invalid
$( "#register-password" ).focusout(function(event) {
  if ($( this ).val() === $( "#register-password-confirm" ).val()) {
    $( "#register-password-confirm" ).removeClass("invalid").addClass("valid");
    $( "#register-password-confirm" )[0].setCustomValidity("");
  } else {
    $( "#register-password-confirm" ).removeClass("valid").addClass("invalid");
    $( "#register-password-confirm" )[0].setCustomValidity("Passwords don't match");
  }
});
$( "#register-password-confirm" ).keyup(function() {
  if ($( this ).val() === $( "#register-password" ).val()) {
    $( this ).removeClass("invalid").addClass("valid");
    this.setCustomValidity("");
  } else {
    $( this ).removeClass("valid").addClass("invalid");
    this.setCustomValidity("Passwords don't match");
  }
});
