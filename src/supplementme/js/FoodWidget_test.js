require([
    "dojo/ready", "dojo/_base/declare", "dojo/query", "dijit/registry", "dojo/_base/array",
    "doh/runner", "dojo/dom-attr", "dojo/on", "supplementme/main", "supplementme/test",
    "dojo/domReady!"
], function (ready, declare, query, registry, array, runner, domAttr,on, main, test) {
    declare("supplementme.FoodWidget_test", supplementme.test, {
        constructor: function(args){
            declare.safeMixin(this, args);
            this.suite = "food widget tests";
        },
        setUp: function(){
            this.foodWidgetDomNode = query('.food-widget')[0];
            this.foodWidget = registry.byNode(this.foodWidgetDomNode);
            this.nutrientWidget = this.foodWidget.nutrientWidget;
            this.set_nutrient_form(this.foodWidget.nutrientWidget);
        },
        tests: {
            "should be visible": function(){
                doh.assertTrue(this.foodWidgetDomNode);
            },
            "should add nutrients on click add": function(){
                var nutrientAddBtn = query('.add-nutrients-button')[0];
                on.emit(nutrientAddBtn, "click", {
                    bubbles: true,
                    cancelable: true
                });
                doh.assertTrue(query(
                    'li', this.foodWidget.nutrientsList).length > 0);
            },
            "should save food on click save":function(){
                var foodSaveBtn = query('.save-food-button')[0];
                on.emit(foodSaveBtn, "click", {
                    bubbles: true,
                    cancelable: true
                });
            }
        }
    });
    ready(function () {
        var testsuite = new supplementme.FoodWidget_test();
        testsuite.registerTests();
        doh.run();
    });
});
