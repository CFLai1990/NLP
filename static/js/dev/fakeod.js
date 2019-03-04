const MESSAGE = 'OD_Data'
const FAKEDATA_PIE = {
  'axes': [],
  'labels': ['Samsung', '21%', 'Apple', '14%', 'Huawei', '10%', 'Others', '55%'],
  'legends': []
}

const FAKEDATA_BAR = {
  'axes': [
    {
      'label': ['Sales (In Millions)'],
      'ticks': ['0', '50', '100', '150', '200', '250', '300', '350', '400', '450']
    }, {
      'label': ['Year'],
      'ticks': ['2013', '2014', '2015', '2016', '2017']
    }
  ],
  'labels': [],
  'legends': [
    {
      'label': ['Samsung'],
      'feature': {'color': 'blue'}
    }, {
      'label': ['Apple'],
      'feature': {'color': 'orange'}
    }, {
      'label': ['Huawei'],
      'feature': {'color': 'green'}
    }
  ]
}

class FakeOD {
  constructor (socket) {
    this.socket = socket
    this.message = MESSAGE
    this.data = FAKEDATA_PIE
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
