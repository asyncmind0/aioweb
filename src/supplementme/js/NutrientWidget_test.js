require([
    "dojo/ready",
    "dojo/query",
    "dijit/registry",
    "dojo/_base/array",
    "doh/runner",
    "dojo/dom-attr",
    "dojo/on",
    "supplementme/main",
    "supplementme/test"
], function (ready, query, registry, array, runner, domAttr,on, main, test) {
    ready(function () {
        describe("nutrient widget", function(){
            beforeEach(function(done) {
                this.nutrientWidgetDomNode = query('.nutrient-widget')[0];
                var t = test();
                t.set_nutrient_form(registry.byNode(this.nutrientWidgetDomNode));
                /*dict is empty
                http://stackoverflow.com/questions/6072590/how-to-match-an-empty-dictionary-in-javascript
                */
                Object.prototype.isEmpty = function() {
                    for (var prop in this) if (this.hasOwnProperty(prop)) return false;
                    return true;
                };
                setTimeout(function() {
                    done();
                }, 1000);
            });
            it("should be visible",
               function(){
                   expect(this.nutrientWidgetDomNode).not.toBeNull();
               });
            it("should have nutrients store loaded",function(done){
                expect(this.nutrientStore.data.length).toBeGreaterThan(0);
                done();
            });
            it("should add nutrients to list on click add",function(done){
                var nutrientAddBtn = query('.add-nutrients-button')[0];
                var myself = this;
                on(this.nutrientWidget, "AddNutrient", function(data){
                    expect(myself.nutrientWidget.foodNutrients.isEmpty()).toBe(false);
                    done();
                });
                on.emit(nutrientAddBtn, "click", {
                     bubbles: true,
                     cancelable: true
                });
            });
        });
    });
});
