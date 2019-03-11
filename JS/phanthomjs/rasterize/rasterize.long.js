//"use strict";
// example debug:
// phantomjs --debug=true --local-to-remote-url-access=true --web-security=no ~/scripts/js/rasterize.js http://www.google.com google.png 1920px

var page = require('webpage').create(),
    system = require('system'),
    address, output, size;
    dpi = 72;  //this constant factor can't be change.
    //page.settings.resourceTimeout=6000
	
if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: rasterize.js URL filename [paperwidth*paperheight|paperformat] [zoom]');
    console.log('  paper (pdf output) examples: "5in*7.5in", "10cm*20cm", "A4", "Letter"');
    console.log('  image (png/jpg output) examples: "1920px" entire page, window width 1920px');
    console.log('                                   "800px*600px" window, clipped to 800x600');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: 600, height: 600 };
    if (system.args.length > 3 && system.args[2].substr(-4) === ".pdf") {
        size = system.args[3].split('*');
        //wavefancy@gmail.com, hacker here for set size as in.
        pw = parseFloat(size[0], 10) * dpi;
        ph = parseFloat(size[1], 10) * dpi;
        //console.log(pw)
        
        page.viewportSize = { width: pw , height: ph };
        page.paperSize = size.length === 2 ? { width: pw , height: ph, margin: '0px' }
                                           : { format: system.args[3], orientation: 'portrait', margin: '0cm' };
    } else if (system.args.length > 3 && system.args[3].substr(-2) === "px") {
        size = system.args[3].split('*');
        if (size.length === 2) {
            pageWidth = parseInt(size[0], 10);
            pageHeight = parseInt(size[1], 10);
            page.viewportSize = { width: pageWidth, height: pageHeight };
            page.clipRect = { top: 0, left: 0, width: pageWidth, height: pageHeight };
        } else {
            console.log("size:", system.args[3]);
            pageWidth = parseInt(system.args[3], 10);
            pageHeight = parseInt(pageWidth * 3/4, 10); // it's as good an assumption as any
            console.log ("pageHeight:",pageHeight);
            page.viewportSize = { width: pageWidth, height: pageHeight };
       }
    }
    if (system.args.length > 4) {
        page.zoomFactor = system.args[4];
    }
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            phantom.exit(1);
        } else {
            window.setTimeout(function () {
                page.render(output);
                phantom.exit();
            //}, 200);
            // Fix the problem of:
            // 2019-02-25T14:28:49 [DEBUG] Network - Resource request error: QNetworkReply::NetworkError(OperationCanceledError) ( "Operation canceled" ) URL: "http://10.200.102.68:8000/json/json.SCZ-1-150510660.json?results/?filter=analysis%20in%203%20and%20chromosome%20in%20%20'1'%20and%20position%20ge%20150010660%20and%20position%20le%20151010660"
            // Ref: https://github.com/ariya/phantomjs/issues/12750
            // jo-37's solution.
            }, 60000);
        }
    });
}
