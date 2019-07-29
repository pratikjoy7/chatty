$(document).ready(function(){
	var socket = io.connect('http://' + document.domain + ':' + location.port)
	var privateSocket = io('http://' + document.domain + ':' + location.port + '/private')
	socket.on('connect', () => {
		privateSocket.emit('user_session', $('meta[name=email]').attr("content"))
	});
	$('#action_menu_btn').click(function(){
		$('.action_menu').toggle();
	});

	$(".contacts_body ui li").click(function(){
		$(".contacts_body ui li").parent().find('li').removeClass("active");
		$(this).addClass("active");
	});
});
