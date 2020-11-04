var http = require('http');

//create a server object:
http.createServer(function (req, res) {
    console.log(req.headers);
    res.write(
        JSON.stringify({
            ts: new Date().getTime(),
            msg: 'Hello World!',
        })
    ); //write a response to the client
    res.end(); //end the response
}).listen(8000); //the server object listens on port 8080
