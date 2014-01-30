require([
    "dojo/ready", "dojo/query", "dijit/registry", "dojo/_base/array",
    "doh/runner", "dojo/dom-attr", "dojo/on", "supplementme/main", "supplementme/test"
], function (ready, query, registry, array, runner, domAttr,on, main, test) {
    ready(function () {
        describe("nutrient widget", function(){
            beforeEach(function(done) {
                this.foodWidgetDomNode = query('.food-widget')[0];
                this.foodWidget = registry.byNode(this.foodWidgetDomNode);
                this.nutrientWidget = this.foodWidget.nutrientWidget;
                test.set_nutrient_form(this.foodWidget.nutrientWidget);
                setTimeout(function() {
                    done();
                }, 1000);
            });
            it("should be visible", function(){
                   expect(this.foodWidgetDomNode).not.toBeNull();
               });
            it("should add nutrients on click add",function(done){
                var nutrientAddBtn = query('.add-nutrients-button')[0];
                on.emit(nutrientAddBtn, "click", {
                     bubbles: true,
                     cancelable: true
                });
                var no = expect(query(
                    'li', this.foodWidget.nutrientsList).length).toBeGreaterThan(0);
                done();
            });
            it("should save food on click save",function(done){
                var foodSaveBtn = query('.save-food-button')[0];
                on.emit(foodSaveBtn, "click", {
                     bubbles: true,
                     cancelable: true
                });
                expect(false).toBe(true);
                done();
            });
        });
    });
});
