import ClientIO from './csocketio.js'
import MSocket from './msgsocket.js'
/* message:
  'Test': get the nlp of the text
*/
const MESSAGE = 'Test'
const MACHINE = 'dl'
let $ = window.$

$(document).ready(function () {
    // Socket.io demo
  let socket = new ClientIO({
    'address': MACHINE,
    'port': 2019,
    'namespace': 'api/annotation'
  })
  let fsocket = new MSocket(socket, MESSAGE)
  socket.on('connect', () => {
      // add more callbacks if necessary
    fsocket.onConnect()
  })
})
