import MLoad from './msguploader.js'

class MSocket {
  constructor (socket) {
    this.socket = socket
    this.message = 'Test'
    this.data = null
    this.mload = new MLoad()
  }
  getData (data) {
    this.data = data
  }
  handleEmit () {
    this.socket.emit(this.message, this.data)
    console.info(`Message '${this.data}' sent!`)
  }
  handleUpload () {
    this.mload.bind('upload', (data) => {
      this.getData(data)
      if (this.data !== null) {
        this.handleEmit()
      }
    })
  }
  handleReceive () {
    this.socket.on(this.message, function (data) {
      console.log(data)
    })
  }
  callback () {
    this.handleUpload()
    this.handleReceive()
  }
}

export default MSocket
