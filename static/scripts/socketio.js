document.addEventListener("DOMContentLoaded", () => {
  var socket = io.connect("/");

  let room = "Principal";
  joinRoom("Principal");

  //Mostrar mensajes
  socket.on("message", data => {
    const p = document.createElement("p");
    const span_username = document.createElement("span");
    const span_timestamp = document.createElement("span");
    const br = document.createElement("br");

    if (data.username) {
      span_username.innerHTML = data.username;
      span_timestamp.innerHTML = data.time_stamp;
      p.innerHTML =
        span_username.outerHTML +
        ": " +
        data.msg +
        br.outerHTML +
        span_timestamp.outerHTML;
      document.querySelector("#display-message-section").append(p);
    } else {
      printSysMsg(data.msg);
    }
  });

  //Send message

  document.querySelector("#send_message").onclick = () => {
    if (document.querySelector("#user_message").value != "") {
      socket.send({
        msg: document.querySelector("#user_message").value,
        username: username,
        room: room
      });
    };


    //Clear input area
    document.querySelector('#user_message').value = '';
  };

  //Room selection.
  document.querySelectorAll(".select-room").forEach(p => {
    p.onclick = () => {
      let newRoom = p.innerHTML;
      if (newRoom == room) {
        msg = `Ya estás en la sala ${room}.`;
        printSysMsg(msg);
      } else {
        leaveRoom(room);
        joinRoom(newRoom);
        room = newRoom;
      }
    };
  });
  //Leave room
  function leaveRoom(room) {
    socket.emit("leave", { username: username, room: room });
  }

  //Join room
  function joinRoom(room) {
    socket.emit("join", { username: username, room: room });
    // Limpiar area de mensajes
    document.querySelector('#display-message-section').innerHTML = "";
    // Autofocus
    document.querySelector('#user_message').focus();
  }

  //Imprimir mensaje de sistema
  function printSysMsg(msg) {
    const p = document.createElement("p");
    p.innerHTML = msg;
    document.querySelector("#display-message-section").append(p);
  }
});
