console.log("is this thing on");
var selected_fit;
$('.ShipType').click(function(){
    console.log("test");
    $(this).find('span').text(function(_, value){return value=='-'?'+':'-'});
    $(this).nextUntil('tr.ShipType').css('display', function(i,v){
	return this.style.display === 'table-row' ? 'none' : 'table-row';
    });
});
$('.ShipName').click(function() {
    var selected = $(this).hasClass("highlight");
    $('.ShipName').removeClass("highlight");
    selected_fit = undefined;
    if(!selected) {
	selected_fit = JSON.parse($(this).attr("data-fit"));
	$(this).addClass("highlight");
    }
});


$('#fit_form').submit(function(ev) {
    ev.preventDefault(); // to stop the form from submitting
    if (selected_fit === undefined) {
	$("#report_text").css('color', 'red');
	$("#report_text").text("Please select fit");
	return;
    }
    var evep_url = $('[name="evep_url"');
    var cargo_size = $('[name="cargo_size"');
    if (evep_url.val() === '') {
	$("#report_text").css('color', 'red');
	$("#report_text").text("Error, empty url");
	return;
    }
    if (cargo_size.val() === '') {
	$("#report_text").css('color', 'red');
	$("#report_text").text("Error, cargo size");
	return;
    }
    var values = {
	'fit': selected_fit,
	'evep_url' : evep_url.val(),
	'cargo_size' : cargo_size.val()
    };
    $("#report_text").css('color', 'gray');
    $("#report_text").text("Working...");
    $.ajax({
	type: "POST",
	url: "/gen_fit",
	data: JSON.stringify(values),
	contentType: "application/json; charset=utf-8",
	dataType: "json",
	success: function(data) {
	    $("#report_text").text("Success: " + data.msg + "\n" +
				   "Added " + data.count + " unique items worth " + data.val + " isk.");
	    $("#report_text").css('color', 'blue');
	},
	error: function(errMsg) {
	    $("#report_text").text("Error " + errMsg.status + ": " + JSON.parse(errMsg.responseText).msg);
	    $("#report_text").css('color', 'red');
	},
	complete: function() {console.log("complete");}
    });
});
