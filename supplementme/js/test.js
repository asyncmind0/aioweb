console.log("loaded");
//require([ 'custom/thinger' ], function(thinger){ … });
require([
    "dojo/ready",
    "supplementme/test_main",
    "supplementme/main_test"
],
        function (ready) {
            ready(function () {
                // Set up the HTML reporter - this is responsible for
                // aggregating the results reported by Jasmine as the
                // tests and suites are executed.
                jasmine.getEnv().addReporter(
                    new jasmine.HtmlReporter()
                );
                // Run all the loaded test specs.
                jasmine.getEnv().execute();
            });
        });
