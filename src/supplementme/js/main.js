require([
    "dojo/_base/declare",
    "dijit/_WidgetBase", "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dijit/_OnDijitClickMixin",
    "dojo/store/JsonRest", 
    "dojo/store/Memory",
    "dojo/store/Cache",
    "dojo/store/Observable",
    "dojo/ready", "dojo/parser", "dijit/form/Form",
    "dijit/form/FilteringSelect",
    "dijit/form/TextBox",
    "dijit/form/NumberSpinner",
    "dijit/form/Select",
    "dojo/json",
    "dojo/when",
    "dojo/on",
    "dojo/dom-construct",
    "dojo/request",
    "dojo/text!supplementme/foodwidget.html", 
    "dojo/text!supplementme/mealwidget.html", 
], function(declare, _WidgetBase,
            _TemplatedMixin, _WidgetsInTemplateMixin,
            _OnDijitClickMixin,
            JsonRest,
            Memory,
            Cache,
            Observable,
            ready, parser, Form,
            FilteringSelect,
            TextBox,
            NumberSpinner,
            Select,
            json,
            when,on,
            domConstruct,
            request,
            food_template,
            meal_template
           ){

    declare("supplementme.Main", null, {
        user: 'anonymous',
        constructor: function(args){
            declare.safeMixin(this, args);
        }
    });
    declare("supplementme.Meal", null, {
        id: 'mealid',
        saved: false,
        foods: [],
        user: 'anonymous',
        constructor: function(args){
            declare.safeMixin(this, args);
        }
    });

    declare("supplementme.FoodWidget",
            [_WidgetBase, _TemplatedMixin, 
             _WidgetsInTemplateMixin, _OnDijitClickMixin,
             JsonRest, Memory, Cache, Observable
            ], {
                templateString: food_template,
                constructor: function(args){
                    declare.safeMixin(this, args);
                    this.foodNutrients = {};
                    var foodStore = new JsonRest({
                        idProperty: '_id',
                        target: "/food/"
                    });
                    this.foodStore = new Memory({ 
                        idProperty: '_id',
                    });
                    this.foodStoreCache = new Cache(foodStore, this.foodStore);
                    this.foodStoreCache.query({'_id':''});
                    debugger
                    var nutrientStore = new JsonRest({
                        target: "/nutrients/",
                    });
                    this.nutrientStore = new Memory();
                    this.nutrientStoreCache = new Cache(nutrientStore, this.nutrientStore);
                    this.nutrientStoreCache.query({id:""});
                },
                startup: function (){
                    var myself = this;
                    this.inherited(arguments);
                    // load cache
                    this.nutrientFilteringSelect = new FilteringSelect({
                        store: this.nutrientStore,
                        required: false,
                        invalidMessage:"Please add some nutrients.",
                        tooltipPosition: ["below"],
                        isValid:function(){
                            var value = myself.nutrientFilteringSelect.get('value');
                            if(value){return true;}
                            return myself.foodNutrients.length === 0?false:true;
                        }
                    }, this.nutrientsSelect);
                    this.foodFilteringSelect = new FilteringSelect({
                        store: this.foodsStore,
                    }, this.foodSelect);
                    this.nutrientFilteringSelect.startup ();
                    this.foodFilteringSelect.startup ();
                    on(this.saveFoodForm, 'submit', this.onSaveFoodForm);
                },
                onSaveFoodForm: function(){
                    this.nutrientFilteringSelect.reset();
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
                onAddNutrient: function(e){
                    var value = this.nutrientFilteringSelect.get('value');
                    var label = this.nutrientFilteringSelect.get('displayedValue');
                    var qty = this.nutrientQuantity.get('value');
                    var unit = this.nutrientUnit.get('value');
                    if(!value || dojo.indexOf(this.foodNutrients, value) >= 0){return;}
                    this.nutrientFilteringSelect.reset();
                    this.foodNutrients[value]={quantity:qty, unit:unit};
                    domConstruct.place("<li>" + label + "</li>", this.nutrientsList);
                }
            });

    declare("supplementme.MealWidget",
            [_WidgetBase, _TemplatedMixin, 
             _WidgetsInTemplateMixin, _OnDijitClickMixin,
             JsonRest, Memory, Cache, Observable, supplementme.FoodWidget
            ], {
                templateString: meal_template,
                constructor: function(args){
                    declare.safeMixin(this, args);
                    var masterStore = new JsonRest({
                        target: "/meal/"
                    });
                    var cacheStore = new Memory({ });
                    this.mealStore = new Cache(masterStore, cacheStore);
                    //this.mealStore.query({'name':'test'});
                },
                onSaveMeal: function(e){
                    console.log('onSaveMeal');
                    var meal = e;
                },
                onAddMeal: function(e){
                    console.log('onAddMeal');
                }
            });
    ready(function(){
        parser.parse();
    });
});
