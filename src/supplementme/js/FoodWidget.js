require([
    "dojo/_base/declare", "dijit/_WidgetBase",
    "dijit/_TemplatedMixin", "dijit/_WidgetsInTemplateMixin",
    "dijit/_OnDijitClickMixin", "dojo/store/JsonRest",
    "dojo/store/Memory", "dojo/store/Cache", "dojo/store/Observable",
    "dojo/ready", "dojo/parser", "dijit/form/Form",
    "dijit/form/FilteringSelect", "dijit/form/TextBox",
    "dijit/form/NumberSpinner", "dijit/form/Select", "dojo/json",
    "dojo/when", "dojo/on", "dojo/dom-construct", "dojo/request",
    "supplementme/NutrientWidget",
    "dojo/text!supplementme/foodwidget.html",
], function(declare, _WidgetBase, _TemplatedMixin,
            _WidgetsInTemplateMixin, _OnDijitClickMixin, JsonRest,
            Memory, Cache, Observable, ready, parser, Form,
            FilteringSelect, TextBox, NumberSpinner, Select, json,
            when,on, domConstruct, request, NutrientWidget,
            food_template ){
    declare("supplementme.FoodWidget",
            [_WidgetBase, _TemplatedMixin, 
             _WidgetsInTemplateMixin, _OnDijitClickMixin,
             JsonRest, Memory, Cache, Observable
            ], {
                templateString: food_template,
                constructor: function(args){
                    declare.safeMixin(this, args);
                    var foodStore = new JsonRest({
                        idProperty: '_id',
                        target: "/food/"
                    });
                    this.foodStore = new Memory({ 
                        idProperty: '_id',
                    });
                    this.foodStoreCache = new Cache(foodStore, this.foodStore);
                    this.foodStoreCache.query({'_id':''});
                },
                startup: function(){
                    var myself = this;
                    this.inherited(arguments);
                    // load cache
                    this.foodFilteringSelect = new FilteringSelect({
                        store: this.foodsStore,
                    }, this.foodSelect);
                    this.foodFilteringSelect.startup ();
                    on(this.saveFoodForm, 'submit', this.onSaveFoodForm);

                    on(this.nutrientWidget, 'AddNutrient',  function(data){
                        var data = data.data;
                        domConstruct.place("<li>" + data.label + "</li>", myself.nutrientsList);
                    });
                },
                onSaveFoodForm: function(){
                    this.nutrientWidget.reset();
                    if(!this.saveFoodForm.validate()){return false;}
                    request.post("/food/add", {
                        method:"POST",
                        data:{
                            name:this.foodName.get("value"),
                            serving_size:this.foodQuantity.get("value"),
                            unit:this.foodUnit.get("value"),
                            nutrients:json.stringify(this.foodNutrients)
                        }
                    }).then(function(data){
                        console.log(data);
                    }, function(err){
                        console.log(err);
                    }, function(evt){
                        console.log(evt);
                    });
                    return false;
                },
                onAddFood: function(e){
                    console.log('onAddFood');
                },
            });
});
