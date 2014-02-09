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
    declare("supplementme.Main_test", supplementme.test, {
        constructor: function(args){
            declare.safeMixin(this, args);
            this.suite = "food widget tests";
        },
        setUp: function(){
                this.foodWidgetDomNode = query('.food-widget')[0];
                this.foodWidget = registry.byNode(this.foodWidgetDomNode);
                this.nutrientStore = this.foodWidget.nutrientStore;
                this.foodWidget.nutrientFilteringSelect.set('value', "PROCNT");
                this.foodWidget.foodName.set('value', "TestFood");
                this.foodWidget.nutrientQuantity.set('value', '1.5');
                this.foodWidget.nutrientUnit.set('value', 'mg');
        },
        "should have nutrients store loaded": function(){
                expect(this.nutrientStore.data.length).toBeGreaterThan(0);
        },
        "should add nutrients to food on click add": function(){
            this.foodWidget.onAddNutrient();
            doh.assertTrue(this.foodWidget.foodNutrients.length > 0);
        },
        "should save food on click save": function(){
            //robot.mouseMoveAt(this.foodWidget.addNutrients, 500);
            //robot.mouseClick({left:true}, 500);
            this.foodWidget.onSaveFoodForm();
            /*on.emit(this.foodWidget.saveFood, "mouseup", {
              bubbles: true,
              cancelable: true
              });*/
        }
    });
    ready(function () {
        var testsuite = new supplementme.Main_test();
        testsuite.registerTests();
        doh.run();
    });
});
/*
require([
    "dojo/ready",
    "dojo/query",
    "dijit/registry",
    "dojo/_base/array",
    "dojo/dom-attr",
    "doh/runner",
    "dojo/robot",
], function(
    ready,
    query,
    registry,
    array,
    domAttr,
    doh, 
    robot){
    ready(function(){
        doh.register("doh/robot",{
            name: "dojorobot1",
            timeout: 8900,
            setUp: function(){
                this.foodWidgetDomNode = query('.food-widget')[0];
                this.foodWidget = registry.byNode(this.foodWidgetDomNode);
                this.nutrientStore = this.foodWidget.nutrientStore;
                this.foodWidget.nutrientFilteringSelect.set('value', "PROCNT");
                this.foodWidget.foodName.set('value', "TestFood");
                this.foodWidget.nutrientQuantity.set('value', '1.5');
                this.foodWidget.nutrientUnit.set('value', 'mg');
            },
            runTest: function(){
                var d = new doh.Deferred();
                robot.mouseMoveAt(this.foodWidget.addNutrients, 500);
                robot.mouseClick({left:true}, 500);
                //robot.mouseClick(this.foodWidget.saveFood.domNode);
                //robot.mouseMoveAt(document.getElementById('textbox'), 500);
                //robot.mouseClick({left:true}, 500);
                //robot.typeKeys(" again", 500, 2500);
                robot.sequence(d.getTestCallback(function(){
                    console.log('ok');
                    //doh.is("hi again", document.getElementById('textbox').value);
                }), 900);
                return d;
            }
        });
        doh.run();
    });
});
*/
