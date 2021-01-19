import ClientIO from './csocketio.js'
import MSocket from './msgsocket.js'
/* message:
  'NLP': get the nlp result of the text
*/
const MESSAGE = 'NLP'
const MACHINE = 'local'
// const VERSION = 'dev2'
// const VERSION = 'dev'
const VERSION = 'public'
let $ = window.$

$(document).ready(function () {
    // Socket.io demo
  let port
  switch (VERSION) {
    case 'dev2':
      port = 2017
      break
    case 'dev':
      port = 2018
      break
    case 'public':
      port = 2019
      break
  }
  let socket = new ClientIO({
    'address': MACHINE,
    'port': port,
    'namespace': 'api/annotation'
  })
  let fsocket = new MSocket(socket, MESSAGE)
  socket.on('connect', () => {
      // add more callbacks if necessary
    fsocket.onConnect()
  })
})
