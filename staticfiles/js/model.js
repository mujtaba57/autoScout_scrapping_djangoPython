$(document).ready(function() {
    $("#make").on("change", function() {
      var values = $(this).val().split(',')
      console.log(values)
      $("#model option").hide()
//      for (var i = 0; i < values.length; i++) {
//        var vals = values[i]
//        $("#model option[value=" + vals + "]").show()
//      };
});

     var multipleCancelButton = new Choices('#choices-multiple-remove-button', {
        removeItemButton: true,
        maxItemCount:3
      });
 });