$(document).ready(function() {
   var num_part = $(".part-container").size();
   
   RefreshDeleteListener();
   RefreshABCListener();

  var part_list = $(".part-container").sort(ComparePart);
  var text = $("#id_meta_data")[0].value + "\n";
  var text2 = "";
  for (var i = 0; i < part_list.length; i++) {
     text += $(part_list[i]).children("#part-meta")[0].value + "\n";
     text2 += $(part_list[i]).children("#part-notes")[0].value + "\n";
  };
  $("textarea#abc").text(text + text2);

   $("#part-create").click(function() {
       num_part += 1;
       var text = '<div class="part-container" style="display: block;">\n';
       text += '<input class="form-control" id="part-order" name="part-order-' + num_part + '" type="number" value=0 />\n';
       text += '<textarea class="form-control" id="part-meta" name="part-meta-' + num_part + '"></textarea>\n';
       text += '<textarea class="form-control" id="part-notes" name="part-notes-' + num_part + '"></textarea>\n';
       text += '<input class="hidden" id="deleted" name="part-deleted-' + num_part + '" type="number" value=0 />\n';
       text += '<a href="javascript:void(0);" class="btn btn-warning" id="part-delete">Delete</a>\n';
       text += '</div>';
       $(".part-list-container").append(text);
       $("#part-count").attr("value", num_part);
       RefreshDeleteListener();
       RefreshABCListener();
   });
   
   abc_editor = new ABCJS.Editor("abc", {paper_id: "paper0", warnings_is: "warnings"});
});

function RefreshDeleteListener() {
   $(".part-container #part-delete").off();
   $(".part-container #part-delete").on("click", function() {
       $(this).parent().children("#deleted").attr("value", 1);
       $(this).parent().css("display", "none");
   });
};

function RefreshABCListener() {
  $("#part-order, #part-meta, #part-notes, #id_meta_data").off();
  $("#part-order, #part-meta, #part-notes, #id_meta_data").on("change keyup paste", function() {
      var part_list = $(".part-container").sort(ComparePart);
      var text = $("#id_meta_data").val() + "\n";
      var text2 = "";
      for (var i = 0; i < part_list.length; i++) {
         text += $(part_list[i]).children("#part-meta").val() + "\n";
         text2 += $(part_list[i]).children("#part-notes").val() + "\n";
      };
      $("textarea#abc").text(text + text2);
  });
};


function ComparePart(a, b) {
    var a_order = parseInt($(a).children("#part-order").val());
    var b_order = parseInt($(b).children("#part-order").val());
    return ((a_order < b_order) ? -1 : ((a_order > b_order) ? 1 : 0));
};
