$(document).ready(function() {
   var num_part = $(".part-container").size();
   
   RefreshDeleteListener();
   RefreshABCListener();

  var part_list = $(".part-container").sort(ComparePart);
  var text = "X: 1\nT: " + $("#id_title").val() + "\nM: " + $("#id_meter").val() + "\nK: " + $("#id_key").val() + "\n";
  var text2 = "";
  for (var i = 0; i < part_list.length; i++) {
     var part = $(part_list[i]);
     text += "V: " + part.children("#part-id").val() + " clef=" + part.children("#part-clef").val() + ' name= "' + part.children("#part-name").val() + '"\n';
     text2 += "[V: " + part.children("#part-id").val() + "]" + $(part_list[i]).children("#part-notes").val() + "\n";
  };
  $("textarea#abc").text(text + text2);

   $("#part-create").click(function() {
       num_part += 1;
       var text = '<div class="part-container" style="display: block;">\n';
       text += '<input class="form-control" id="part-order" name="part-order-' + num_part + '" type="number" value=0 />\n';
       text += '<input class="hidden" id="part-id" name="part-id-' + num_part + '" type="number" value=-' + num_part +' />\n';
       text += '<input class="form-control" id="part-clef" name="part-clef-' + num_part + '" type="text" value="treble" />\n';
       text += '<input class="form-control" id="part-name" name="part-name-' + num_part + '" type="text" value="" />\n';
       text += '<textarea class="form-control" id="part-notes" name="part-notes-' + num_part + '"></textarea>\n';
       text += '<input class="hidden" id="deleted" name="part-deleted-' + num_part + '" type="number" value=0 />\n';
       text += '<a href="#" class="btn btn-warning" id="part-delete">Delete</a>\n';
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
       $(this).parent().attr("class", "part-container-deleted");
   });
};

function RefreshABCListener() {
  $("#part-order, #part-clef, #part-name, #part-notes, #id_title, #id_meter, #id_key").off();
  $("#part-order, #part-clef, #part-name, #part-notes, #id_title, #id_meter, #id_key, #part-delete").on("change keyup paste click", function() {
      var part_list = $(".part-container").sort(ComparePart);
      var text = "X: 1\nT: " + $("#id_title").val() + "\nM: " + $("#id_meter").val() + "\nK: " + $("#id_key").val() + "\n";
      var text2 = "";
      for (var i = 0; i < part_list.length; i++) {
         var part = $(part_list[i]);
         text += "V: " + part.children("#part-id").val() + " clef=" + part.children("#part-clef").val() + ' name="' + part.children("#part-name").val() + '"\n';
         text2 += "[V: " + part.children("#part-id").val() + "]" + $(part_list[i]).children("#part-notes").val() + "\n";
      };
      $("textarea#abc").text(text + text2);
  });
};


function ComparePart(a, b) {
    var a_order = parseInt($(a).children("#part-order").val());
    var b_order = parseInt($(b).children("#part-order").val());
    return ((a_order < b_order) ? -1 : ((a_order > b_order) ? 1 : 0));
};
