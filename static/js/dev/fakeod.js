const MESSAGE = 'OD_Data'
const FAKEDATA = {
  'labels': ['Samsung', '21%', 'Apple', '14%', 'Huawei', '10%', 'Others', '55%']
}

class FakeOD {
  constructor (socket) {
    this.socket = socket
    this.message = MESSAGE
    this.data = FAKEDATA
    this.handleReceive()
  }

  handleReceive () {
    this.socket.on(this.message, (data) => {
      console.info(data)
    })
  }

  emit (socket) {
    this.socket.emit(this.message, this.data)
  }
}

export default FakeOD
