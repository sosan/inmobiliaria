(function ($) {

	"use strict";

	
	// Submit loader mask 
	$('form#wrapped').on('submit', function () {
		var form = $("form#wrapped");
		form.validate();
		if (form.valid()) {
			$("#loader_form").fadeIn();
		}
	});
	
	// Float labels
	var floatlabels = new FloatLabels( 'form', {
		    style: 2
	});
	
})(window.jQuery); 