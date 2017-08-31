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
    if(!selected) {
	selected_fit = JSON.parse($(this).attr("data-fit"));
	$(this).addClass("highlight");
    }
});


$('#fit_form').submit(function(ev) {
    ev.preventDefault(); // to stop the form from submitting
    var values = $(this).serialize();
    if (selected_fit === undefined) {
	$("#error_text").text("Please select fit");
	return;
    }
    var evep_url = $('[name="evep_url"');
    var cargo_size = $('[name="cargo_size"');
    if (evep_url.val() === '') {
	$("#error_text").text("Error, empty url");
	return;
    }
    if (cargo_size.val() === '') {
	$("#error_text").text("Error, cargo size");
	return;
    }
    selected_fit["evep_url"] = evep_url.val();
    selected_fit["cargo_size"] = cargo_size.val();
    $.ajax({
	type: "POST",
	url: "/gen_fit",
	data: JSON.stringify(selected_fit),
	contentType: "application/json; charset=utf-8",
	dataType: "json",
	success: function(data) {},
	failure: function(errMsg) {}
    });
});
