require([
    "doh", "doh/runner", "dojo/ready", "dojo/query", "dijit/registry",
    "dojo/_base/array", "dojo/dom-attr", "dojo/on","dojo/json",
    "supplementme/main", "supplementme/test", "dojo/domReady!"
], function (doh, runner, ready, query, registry, array, domAttr,on, JSON,main) {
    ready(function(){
        tester = new supplementme.test();
        function setUp(){
            this.nutrientWidgetDomNode = query('.nutrient-widget')[0];
            this.nutrientWidget = registry.byNode(this.nutrientWidgetDomNode);
            tester.set_nutrient_form(this.nutrientWidget);
            /*dict is empty
              http://stackoverflow.com/questions/6072590/how-to-match-an-empty-dictionary-in-javascript
            */
            Object.prototype.isEmpty = function() {
                for (var prop in this) if (this.hasOwnProperty(prop)) return false;
                return true;
            };
        }
        var tests = {
            "should be visible": function(){
                return doh.assertTrue(this.nutrientWidgetDomNode);
            },
            "should have nutrients store loaded": function(){
                doh.assertTrue(tester.nutrientStore.data.length > 0);
            },
            "should add nutrients to list on click add": function(){
                var nutrientAddBtn = query('.add-nutrients-button')[0];
                var myself = this;
                var deferred = new doh.Deferred();
                on(this.nutrientWidget, "AddNutrient", function(data){
                    doh.assertFalse(myself.nutrientWidget.foodNutrients.isEmpty());
                    deferred.resolve();
                });
                on.emit(nutrientAddBtn, "click", {
                    bubbles: true,
                    cancelable: true
                });
                return deferred;
            }
        };

        tester.registerTests("nutrient widget", tests, setUp);
        doh.run();
    });
});
