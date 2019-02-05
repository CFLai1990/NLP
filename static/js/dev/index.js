import io from 'socket.io-client'
import $ from 'jquery'
window.$ = $

let callbackCreator = function (socket) {
  let callback = function () {
    socket.on('Test', function (msg) {
      console.log(msg)
    })
    $('#nlptest-submit').on('click', function () {
      let text = $('#nlptest-input').val()
      if (text !== '' || undefined) {
        socket.emit('Test', text)
      }
    })
  }
  return callback
}

$(document).ready(function () {
    // Socket.io demo
  let socket = io('http://localhost:2019/api/annotation')
  socket.on('connect', callbackCreator(socket))
})
