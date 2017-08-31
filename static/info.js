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
	selected_fit = $(this).attr("data-fit");
	$(this).addClass("highlight");
    }
});


$('#fit_form').submit(function(ev) {
    ev.preventDefault(); // to stop the form from submitting
    var values = $(this).serialize();
    /* Validations go here */
    jQuery.post("gen_fit", /*pass args*/null, function(data, status, jqxhr) {}, 'text/json')
});
