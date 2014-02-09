require([
    "dojo/ready",
"dojo/_base/declare", 
    "dojo/query",
    "dijit/registry",
    "dojo/_base/array",
    "doh/runner",
    "dojo/dom-attr",
    "dojo/on",
    "supplementme/main",
    "supplementme/test",
    "dojo/domReady!"
], function (ready, declare, query, registry, array, runner, domAttr,on) {
    declare("supplementme.MealWidget_test", supplementme.test, {
        constructor: function(args){
            declare.safeMixin(this, args);
            this.suite = "meal widget tests";
        },
        setUp: function(){
                this.mealWidgetDomNode = query('.meal-widget')[0];
            },
        "should be visible": function(){
            expect(this.mealWidgetDomNode).not.toBeNull();
        }
    });
    ready(function () {
        var testsuite = new supplementme.MealWidget_test();
        testsuite.registerTests();
        doh.run();
    });
});
