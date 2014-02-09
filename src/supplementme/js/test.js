require(["doh", "dojo/_base/declare", "dojo/ready", "dojo/query",
    "dijit/registry", "dojo/_base/array", "doh/runner",
    "dojo/dom-attr", "dojo/on", "supplementme/main" ], 
function(doh, declare, ready, query, registry, array, runner, domAttr,on) {
    window.jsApiReporter = {};
    doh._report = function(){
        var report = {testCount: this._testCount, groupCount: this._groupCount,
                      errors:this._errorCount, failureCount: this._failureCount};
        var jsonString = JSON.stringify(report);
        console.log(jsonString);
        window.jsApiReporter.status = function(){
            return "done";
        };
        window.jsApiReporter.specs = function(){
            return report;
        };
    };
    declare("supplementme.basetest", [], {
        constructor: function(args){
            declare.safeMixin(this, args);
        },
        registerTests: function(){
            var wrapped = [];
            for(var name in this.tests){
                wrapped.push({
                    name: name,
                    setUp: this.setUp,
                    runTest: this.tests[name],
                    timeout:500
                });
            }
            doh.register(this.suite, wrapped);
        }
    });
    declare("supplementme.test", supplementme.basetest, {
        constructor: function(args){
            declare.safeMixin(this, args);
        },
        set_nutrient_form: function(nutrientWidget){
            this.nutrientStore = nutrientWidget.nutrientStore;
            nutrientWidget.nutrientFilteringSelect.set('value', "PROCNT");
            nutrientWidget.nutrientQuantity.set('value', '1.5');
            nutrientWidget.nutrientUnit.set('value', 'mg');
        },
    });
});
