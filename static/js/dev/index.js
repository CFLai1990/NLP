import ClientIO from './csocketio.js'
import MSocket from './msgsocket.js'
/* message:
  'NLP': get the nlp result of the text
*/
const MESSAGE = 'NLP'
const MACHINE = 'dl'
const VERSION = 'dev'
// const VERSION = 'public'
let $ = window.$

$(document).ready(function () {
    // Socket.io demo
  let socket = new ClientIO({
    'address': MACHINE,
    'port': VERSION === 'dev' ? 2018 : 2019,
    'namespace': 'api/annotation'
  })
  let fsocket = new MSocket(socket, MESSAGE)
  socket.on('connect', () => {
      // add more callbacks if necessary
    fsocket.onConnect()
  })
})
