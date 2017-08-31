$('tr.ShipType').click(function(){
    $(this).find('span').text(function(_, value){return value=='-'?'+':'-'});
    $(this).nextUntil('tr.ShipType').css('display', function(i,v){
	return this.style.display === 'table-row' ? 'none' : 'table-row';
    });
});
