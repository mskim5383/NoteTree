$(document).ready(function() {
   var num_part = $(".part-container").size();
   
   RefreshDeleteListener();

   $("#part-create").click(function() {
       num_part += 1;
       var text = '<div class="part-container" style="display: block;">\n';
       text += '<input class="form-control" id="part-order-' + num_part +'" name="part-order-' + num_part + '" type="number" value=0 />\n';
       text += '<input class="form-control" id="part-meta-' + num_part +'" name="part-meta-' + num_part + '" type="text" value=""/>\n';
       text += '<input class="form-control" id="part-notes-' + num_part +'" name="part-notes-' + num_part + '" type="text" value=""/>\n';
       text += '<input class="hidden" id="deleted" name="part-deleted-' + num_part + '" type="number" value=0 />\n';
       text += '<a href="javascript:void(0);" class="btn btn-warning" id="part-delete">Delete</a>\n';
       text += '</div>';
       $(".part-list-container").append(text);
       $("#part-count").attr("value", num_part);
       RefreshDeleteListener();
   });
});

function RefreshDeleteListener() {
   $(".part-container #part-delete").off();
   $(".part-container #part-delete").on("click", function() {
       $(this).parent().children("#deleted").attr("value", 1);
       $(this).parent().css("display", "none");
   });
};
