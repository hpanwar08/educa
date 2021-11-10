$(document).ready(function () {
    const url = 'ws://' + window.location.host + '/ws/chat/room/' + '{{ course.id }}/';
    const chatSocket = new WebSocket(url);

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        const dateOptions = {hour: 'numeric', minute: 'numeric', hour12: true};
        const datetime = new Date(data['datetime']).toLocaleString('en', dateOptions);
        const isMe = data.user === '{{request.user}}';

        const name = isMe ? 'Me' : data.user;
        const $chat = $('#chat');

        const msgSourceBG = isMe ? 'chat-bg-me' : 'chat-bg-other';
        const msgAlignSource = isMe ? 'justify-content-end' : '';

        $chat.append(
            '<div class="w-100 d-inline-flex mb-2 ' + msgAlignSource + '">' +
            '<div class="w-75 p-2 text-break ' + msgSourceBG + '"><small class="fw-lighter">' + name + '<span class="fst-italic"> ' + datetime + '</span></small><br>' + message + '</div>' +
            '</div>'
        );
        $chat.scrollTop($chat[0].scrollHeight);

    };

    chatSocket.onclose = function (e) {
        console.log('Chat socket closed unexpectedly')
    };

    const $input = $('#chat-message-input');
    const $submit = $('#chat-message-submit');

    $submit.click(function () {
        const message = $input.val();
        if (message) {
            chatSocket.send(JSON.stringify({'message': message}));
            $input.val('');
            $input.focus();
        }
    });

    $input.focus();
    $input.keyup(function (e) {
        if (e.keyCode === 13) {
            $submit.click()
        }
    });
});