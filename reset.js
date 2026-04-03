module.exports = {
  run: [{
    when: "{{exists('INSTALLATION_COMPLETE.txt')}}",
    method: "fs.rm",
    params: {
      path: "INSTALLATION_COMPLETE.txt",
    },
  }, {
    method: "fs.rm",
    params: {
      path: "env",
    },
  }],
}
