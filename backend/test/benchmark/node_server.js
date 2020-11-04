var http = require('http');

var lastTime = new Date().getTime();
//create a server object:
http.createServer(function (req, res) {
    console.log(req.headers);
    let now = new Date().getTime();
    let ret = JSON.stringify({
        ts: now,
        duration: (now - lastTime) / 1000,
        msg: 'Hello World!',
    });
    lastTime = now;
    console.log(ret);
    res.write(ret); //write a response to the client
    res.end(); //end the response
}).listen(8000); //the server object listens on port 8080
