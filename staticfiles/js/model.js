
$(document).ready(function() {
     var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
        removeItemButton: true,
        maxItemCount:3
      });

     $('#submit_btn').submit(function(){
        alert("hey boi")
        $.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
            success: function(response) { // on success..
                alert("hey boi") // update the DIV
            }
        });
        return false;
     });
 });