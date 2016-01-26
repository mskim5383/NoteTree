$(document).ready(function() {
    $("#star").on("click", function() {
        $.ajax(
        {
            url : "star/",
            type : "POST",
            data : {csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()},
            dataType : "json",
            success : function(data){
                console.log(data.status);
                if(data.status == "star"){
                    $(this).attr("class", "star");
                }
                else if(data.status == "unstar"){
                    $(this).attr("class", "unstar");
                }
            }
        });
    });
});
