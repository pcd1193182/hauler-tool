$('tr.header').click(function(){
    $(this).find('span').text(function(_, value){return value=='-'?'+':'-'});
    $(this).nextUntil('tr.header').css('display', function(i,v){
	return this.style.display === 'table-row' ? 'none' : 'table-row';
    });
});
