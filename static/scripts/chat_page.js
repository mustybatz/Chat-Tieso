document.addEventListener('DOMContentLoaded', () => {
    //Enter para mandar mensaje.
    let msg = document.querySelector('#user_message');
    msg.addEventListener('keyup', function(event) {
        event.preventDefault();
        if (event.keyCode === 13){
            document.querySelector('#send_message').click();
        }
    })
})