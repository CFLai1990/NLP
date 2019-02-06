import io from 'socket.io-client'
import MSocket from './msgsocket.js'
let $ = window.$
let VERSION = 'dl'

$(document).ready(function () {
    // Socket.io demo
  let socket
  switch (VERSION) {
    case 'local':
      socket = io('http://localhost:2019/api/annotation')
      break
    case 'db':
      socket = io('http://192.168.10.9:2019/api/annotation')
      break
    case 'dl':
      socket = io('http://192.168.10.21:2019/api/annotation')
      break
    case 'public':
      break
  }
  let msocket = new MSocket(socket)
  socket.on('connect', () => { msocket.callback() })
})
