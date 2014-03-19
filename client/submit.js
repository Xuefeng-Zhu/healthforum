document.getElementById("submitForm").onclick = function() {  
  $.post( "/test", { s: $("#drugName").val() }, function( data ) {
  	  if(data == null)
  	  	return;
	  alert("RECEIVED MESSAGE: " + data);
  });
};

