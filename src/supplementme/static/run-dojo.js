var page = require('webpage').create(),url, text;

if (!require('system').isSSLSupported) {
    console.log('Need SSL');
    phantom.exit();
} else {
    console.log('Have SSL');
}

// set support for cookies
phantom.cookiesEnabled = true;
var debugx=false;

page.onConsoleMessage = function (msg) {
    console.log(msg);
};

page.onError = function(msg, trace) {
    console.log("Error Encountered: " + msg);
};

page.onInitialized = function() {
    page.evaluate(function() {
        document.addEventListener("DOMContentLoaded", function() {
            console.log("DOM content has loaded.");
        }, false);
    });
};

page.onResourceRequested = function(request) {
    if (debugx) console.log("Request (#" + request.id + "): " + JSON.stringify(request));
};

page.onResourceReceived = function(response) {
    if (debugx) console.log('Response (#' + response.id + ', stage "' + response.stage + '"): ' + JSON.stringify(response));
};


// must have URL to hit
url = phantom.args[0];
if (typeof url === "undefined") {
    console.log("Error: arg[0] must be a fully qualified URL.\nCommand format is: 'phantomjs phantomDohRunner.js \"URL\" [timeout in millis]'."); 
    console.log("For Example:\nphantomjs phantomDohRunner.js \"http://HOST/tester/dojo/util/doh/runner.html?test=dojo/tests/_base/array\" 20000\n\n");        
    // phantom.exit doesn't terminate the program, so put in conditional
    phantom.exit();
} else {
    
    // get timeout from command line or default
    timeout = phantom.args[1];
    if (typeof timeout === "undefined") {
        timeout = 10000; // default to 1 minute
    }
    
    console.log("URL = " + url);
    console.log("Timeout = " + timeout + " milliseconds\n\n");
    
    page.open(url, function () {
        
        setTimeout(function(){
            page.render("phantomDohRunnerFinish.png");
            console.log("Closing down.");
            phantom.exit();
        }, timeout);
        
    });
}
