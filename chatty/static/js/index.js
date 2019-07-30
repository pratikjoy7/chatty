$(document).ready(function(){
	const socket = io.connect('http://' + document.domain + ':' + location.port);
	const privateSocket = io('http://' + document.domain + ':' + location.port + '/private');

	socket.on('connect', () => {
		privateSocket.emit('user_session', $('meta[name=email]').attr("content"))
	});

	$('#action_menu_btn').click(function() {
		$('.action_menu').toggle();
	});

	$(".contacts_body ui li").click(function() {
		$(".contacts_body ui li").parent().find('li').removeClass("active");
		$(this).addClass("active");
		$(".msg_head .bd-highlight .user_info span").text('Chat with ' + $(".active span").text());
		$(".msg_head .bd-highlight .img_cont img").attr('src', $(".active .img_cont img").attr('src').toString());
		$(".card-footer").children().removeClass("unclickable");
	});

	$(".send_btn").click(() => {
		const sender = $('.active .user_info p').text();
		const recipient = $('meta[name=email]').attr("content");
		const message = $(".type_msg").val();

		privateSocket.emit('message_sent', {
			'sender': sender,
			'recipient': recipient,
			'message': message
		});

		$(".type_msg").val('')
	});

	privateSocket.on('new_private_message', function(message) {
		
	});
});
