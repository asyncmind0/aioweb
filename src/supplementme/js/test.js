require(["doh", "dojo/_base/declare", "dojo/ready", "dojo/query",
    "dijit/registry", "dojo/_base/array", "doh/runner",
    "dojo/dom-attr", "dojo/on", "supplementme/main" ], 
function(doh, declare, ready, query, registry, array, runner, domAttr,on) {
    declare("supplementme.test", [], {
        constructor: function(args){
            declare.safeMixin(this, args);
        },
        set_nutrient_form: function(nutrientWidget){
            nutrientStore = nutrientWidget.nutrientStore;
            nutrientWidget.nutrientFilteringSelect.set('value', "PROCNT");
            nutrientWidget.nutrientQuantity.set('value', '1.5');
            nutrientWidget.nutrientUnit.set('value', 'mg');
        }
    });
});
