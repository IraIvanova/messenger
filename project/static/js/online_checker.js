function updateUsersStatus() {
    const statusElements = document.querySelectorAll('.user-status');
    const chatId = document.getElementsByClassName('chat-heading')[0].dataset.chat;
    const response = axios.post(`/get_user_statuses/${chatId}/`, {}, {
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
        })
        .then(response => {
            if (response.status === 200) {
                statuses = response.data;

                statusElements.forEach(function(element) {
                    const online = statuses[element.getAttribute('data-user-id')];
                    element.innerText = online ? ' - ONLINE' : ' - OFFLINE';
                });
            }
        });
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function() {
    setInterval(function() {
        updateUsersStatus();
    }, 5000);
});