$(document).ready(function () {
    const url = 'ws://' + window.location.host + '/ws/chat/room/' + '{{ course.id }}/';
    const chatSocket = new WebSocket(url);

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const message = data.message;
        const $chat = $('#chat');
        $chat.append('<div class="w-75 mb-3"><div class="d-inline-flex p-2 text-break bg-light ">' + message + '</div></div><br>');
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