require([
    "dojo/ready",
    "dojo/query",
    "dijit/registry",
    "dojo/_base/array",
    "doh/runner",
    "dojo/dom-attr",
    "dojo/on",
    "supplementme/main"
], function (ready, query, registry, array, runner, domAttr,on) {
    ready(function () {
        describe("meal widget", function(){
            it("should be visible",
               function(){
                   expect(query('.meals-widget').length).toEqual(1);
               });
            it("should add selected meal to list of meals",
               function(){
               });
        });
        describe("on clicking save", function(){
            it("should save meal to saved meals",
               function(){
               });
        });
        describe("food widget", function(){
            beforeEach(function(done) {
                this.foodWidgetDomNode = query('.food-widget')[0];
                this.foodWidget = registry.byNode(this.foodWidgetDomNode);
                this.nutrientStore = this.foodWidget.nutrientStore;
                this.foodWidget.nutrientFilteringSelect.set('value', "PROCNT");
                this.foodWidget.foodName.set('value', "TestFood");
                this.foodWidget.nutrientQuantity.set('value', '1.5');
                this.foodWidget.nutrientUnit.set('value', 'mg');
                setTimeout(function() {
                    done();
                }, 1000);
            });
            it("should have nutrients store loaded",function(done){
                expect(this.nutrientStore.data.length).toBeGreaterThan(0);
                done();
            });
            it("should add nutrients to food on click add",function(done){
                this.foodWidget.onAddNutrient();
                expect(this.foodWidget.foodNutrients.length).toBeGreaterThan(0);
                done();
            });
            it("should save food on click save",function(done){
                //robot.mouseMoveAt(this.foodWidget.addNutrients, 500);
                //robot.mouseClick({left:true}, 500);
                this.foodWidget.onSaveFoodForm();
                /*on.emit(this.foodWidget.saveFood, "mouseup", {
                    bubbles: true,
                    cancelable: true
                });*/
                done();
            });
        });
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
