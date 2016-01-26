$(document).ready(function() {
    $("#star").on("click", function() {
        var star = $(this);
        $.ajax(
        {
            url : "star/",
            type : "POST",
            data : {csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()},
            dataType : "json",
            success : function(data){
                console.log(data.status);
                if(data.status == "star"){
                    star.attr("class", "star");
                    star.html("Unstar");

                }
                else if(data.status == "unstar"){
                    star.attr("class", "unstar");
                    star.html("Star");
                }
            }
        });
    });
    $("#abc").val($(".score-select").attr("value"));
   abc_editor = new ABCJS.Editor("abc", {paper_id: "paper0", midi_id: "midi", warnings_is: "warnings"});
   
   $(".part-select, .score-select").on("click", function() {
       $("#abc").val($(this).attr("value"));
       $(this).parent().parent().children(".active").attr("class", "");
       $(this).parent().attr("class", "active");
   });
   $("#midi-play").on("click", function() {
       var midi = $("#midi").children("a").attr("href");
       MIDI.player.loadFile(midi, player.start);
       MIDI.player.start();
   });
});
