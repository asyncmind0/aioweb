require([
    "dojo/ready",
    "dojo/query",
    "supplementme/main"
], function (ready, query) {
    describe("meal widget", function(){
        it("should be visible",
           function(){
               expect(query('.meals-widget').length).toEqual(1);
           });
    });
    describe("on clicking add", function(){
        it("should add selected meal to list of meals",
           function(){
           });
    });
    describe("on clicking save", function(){
        it("should save meal to saved meals",
           function(){
           });
    });
});
