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

	$("#encrypt_msg").click(() => {
		$("#encrypt_msg span").toggleClass("encrypt_btn_active");
	});

	$(".send_btn").click(() => {
		let encrypt = $("#encrypt_msg span").hasClass("encrypt_btn_active");

		const sender = $('meta[name=email]').attr("content");
		const recipient = $('.active .user_info p').text();
		const message = $(".type_msg").val();

		privateSocket.emit('message_sent', {
			'encrypt': encrypt,
			'sender': sender,
			'recipient': recipient,
			'message': message
		});

		$(".type_msg").val("");
		$(".msg_card_body h2").remove();
		$(".msg_card_body").append('<div class="d-flex justify-content-end mb-4">' +
										'<div class="msg_cotainer_send">' +
											message +
										'</div>' +
										'<div class="img_cont_msg">' +
											'<img src="' + $("#user_image").attr('src').toString() + '" class="rounded-circle user_img_msg">' +
										'</div>' +
									'</div>');
	});

	privateSocket.on('new_private_message', function(payload) {
		$(".msg_card_body h2").remove();
		$(".msg_card_body").append('<div class="d-flex justify-content-start mb-4">' +
										'<div class="img_cont_msg">' +
											'<img src="' + $(".active .img_cont img").attr('src').toString() + '" class="rounded-circle user_img_msg">' +
										'</div>' +
										'<div class="msg_cotainer">' +
											'<span>' + payload['message'] + '</span>' +
										'</div>' +
									'</div>');
		if (payload.encrypt === true) {
			$(".justify-content-start").append('<button class="decrypt_btn">' +
													'<i class="fas fa-lock-open"></i> Decrypt' +
											   '</button>');
		}
	});

	$('input[type="file"]').change(function(e) {
		let fileName = e.target.files[0].name;
		$('#uploaded-file').append('<b>Selected Private-key: </b>' + fileName);
	});

	$(document).on("click", ".decrypt_btn", function() {
		const encrypted_message = $(this).prev().text();
		let file = document.getElementById("file-input").files[0];
		if (file) {
			let reader = new FileReader();
			reader.readAsText(file, "UTF-8");
			reader.onload = function (evt) {
				privateSocket.emit('decrypt_message', {
					'email': $('meta[name=email]').attr("content"),
					'message': encrypted_message,
					'private_key': evt.target.result
				});
			}
			reader.onerror = function (evt) {
				$.confirm({
					theme: 'Modern',
					closeIcon: true,
					title: 'Error',
					content: 'An error occurred while trying to read your private key, please try again later.',
					type: 'red',
					typeAnimated: true,
					buttons: {
						ok: {
							text: 'Okay',
							action: function () {}
						}
					}
				});
			}
		}
		else {
			$.confirm({
				theme: 'Modern',
				closeIcon: true,
				title: 'Warning',
				content: 'Select your private key for decrypting this message!',
				type: 'orange',
				typeAnimated: true,
				buttons: {
					ok: {
						text: 'Okay',
						action: function () {}
					}
				}
			});
		}
	});

	privateSocket.on('new_decrypted_msg', function(payload) {
		if (payload.message === null) {
			$.confirm({
				theme: 'Modern',
				closeIcon: true,
				title: 'Decryption Failed',
				content: 'Verify if you have selected the right private key and try again!',
				type: 'red',
				typeAnimated: true,
				buttons: {
					ok: {
						text: 'Okay',
						action: function () {}
					}
				}
			});
		}
		else {
			$.confirm({
				theme: 'Modern',
				closeIcon: true,
				title: 'Decrypted Message',
				content: payload['message'],
				type: 'green',
				typeAnimated: true,
				buttons: {
					ok: {
						text: 'Okay',
						action: function () {}
					}
				}
			});
		}
	});
});
