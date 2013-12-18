require([
    "dojo/ready",
    "dojo/query",
    "dijit/registry",
    "dojo/_base/array",
    "supplementme/main"
], function (ready, query, registry, array) {
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
            var foodWidgetDomNode = query('.food-widget')[0];
            var foodWidget = registry.byId(dojo.attr(foodWidgetDomNode, 'widgetid'));
            var nutrientStore = foodWidget.nutrientStore;
            beforeEach(function(done) {
                setTimeout(function() {
                    done();
                }, 100);
            });
            it("should be visible", function(done){
                   expect(query('.food-widget').length).toEqual(1);
                done();
               });
            it("should have nutrients store loaded",function(done){
                   expect(nutrientStore.data.length).toBeGreaterThan(0);
                done();
            });
        });
    });
});
