let edit_btns = document.getElementsByClassName('edit-msg');
let del_btns = document.getElementsByClassName('delete-msg');
let send_btn = document.querySelector('.reply button');
let textarea = document.getElementById('id_message');
let chat_id = document.getElementById('id_chat');
let author_id = document.getElementById('id_author');
let form = document.querySelector('.reply form');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


for (let btn of edit_btns) {
    btn.addEventListener('click', () => {
        textarea.value = btn.parentElement.nextElementSibling.innerText;

        send_btn.addEventListener('click', (e) => {
            e.preventDefault();

            send_request('/edit_message', btn, 'edit')
        });
    });
}

for (let del_btn of del_btns) {
       del_btn.addEventListener('click', (e) => {
            e.preventDefault();

            send_request('/delete_message', del_btn, 'delete')
        });
}

let send_request = (url, btn, type) => {
    axios.post(url,
        {
            'message': textarea.value,
            'author': author_id.value,
            'chat': chat_id.value,
            'message_id': btn.dataset.id
        },
        {
            headers: {"X-CSRFToken": csrftoken}
        }
    ).then((res) => {

        if (res.status === 200) {
            if (type === 'edit') {
            btn.parentElement.nextElementSibling.innerText = textarea.value
            textarea.value = ''
            } else {
                btn.parentElement.parentElement.parentElement.parentElement.remove()
            }
        }
    })
}