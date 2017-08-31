console.log("is this thing on");
$('.ShipType').click(function(){
    console.log("test");
    $(this).find('span').text(function(_, value){return value=='-'?'+':'-'});
    $(this).nextUntil('tr.ShipType').css('display', function(i,v){
	return this.style.display === 'table-row' ? 'none' : 'table-row';
    });
});
$('tr').click(function() { console.log("test1"); });
$('th').click(function() { console.log("test2"); });


$('#fit_form').submit(function(ev) {
    ev.preventDefault(); // to stop the form from submitting
    var values = $(this).serialize();
    /* Validations go here */
    jQuery.post("gen_fit", /*pass args*/null, function(data, status, jqxhr) {}, 'text/json')
});
