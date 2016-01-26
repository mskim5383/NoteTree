$(document).ready(function() {
   $("#abc").val($(".score-select").attr("value"));
   abc_editor = new ABCJS.Editor("abc", {paper_id: "paper0", warnings_is: "warnings"});
   
   $(".part-select, .score-select").on("click", function() {
       $("#abc").val($(this).attr("value"));
       $(this).parent().parent().children(".active").attr("class", "");
       $(this).parent().attr("class", "active");
   });
});
