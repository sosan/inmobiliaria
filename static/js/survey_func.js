jQuery(function ($)
{
	"use strict";
	$("#wizard_container").wizard({
		stepsWrapper: "#wrapped",
		submit: ".submit",
		beforeSelect: function (event, state)
		{
			console.log("state:"+state.isMovingForward);

			if (!state.isMovingForward)
				return true;

			var inputs = $(this).wizard('state').step.find(':input');
			console.log("valid:"+inputs.valid())
			return !inputs.length || !!inputs.valid();
		}
	}).validate({
		errorPlacement: function (error, element) {
			if (element.is(':radio') || element.is(':checkbox')) {
				error.insertBefore(element.next());
			} else {
				error.insertAfter(element);
			}
		}
	});

	$('#wrapped').validate({
		ignore: [],
		rules: {
			select: {
				required: true
			}
		},
		errorPlacement: function (error, element) {
			if (element.is('select:hidden')) {
				error.insertAfter(element.next('.nice-select'));
			} else {
				error.insertAfter(element);
			}
		}
	});
});