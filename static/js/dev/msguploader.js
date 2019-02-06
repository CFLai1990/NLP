let $ = window.$

class MsgUploader {
  constructor () {
    this.input = '#nlptest-input'
    this.submit = '#nlptest-submit'
  }
  bind (event, callback) {
    if (event === 'upload') {
      $(this.submit).on('click', () => {
        let msg = $(this.input).val()
        if (msg === '') { msg = null }
        callback(msg)
      })
    } else {
      $(this.input).on(event, callback)
    }
  }
}

export default MsgUploader
