$(document).ready(function() {
	console.log("ASDAS");
	$('body').on('keypress', '#s', function(e){
		console.log("AHAH");
    	var p = e.which;
    	if(p==13){
    		console.log("HH");
        	window.location.href="/search/?keyword="+$(this).val();
    	}
 	});
 });