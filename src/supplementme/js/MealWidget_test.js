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
        describe("nutrient widget", function(){
            beforeEach(function(done) {
                this.mealWidgetDomNode = query('.meal-widget')[0];
                setTimeout(function() {
                    done();
                }, 1000);
            });
            it("should be visible",
               function(){
                   expect(this.mealWidgetDomNode).not.toBeNull();
               });
        });
    });
});
