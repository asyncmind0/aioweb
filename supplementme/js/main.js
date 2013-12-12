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
    "dojo/when",
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
            when,
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
                    var masterStore = new JsonRest({
                        target: "/food/"
                    });
                    var cacheStore = new Memory({ });
                    this.foodStore = new Cache(masterStore, cacheStore);
                    //this.foodStore.query({'name':'test'});
                    var nutrientStore = new JsonRest({
                        target: "/nutrients/",
                    });
                    this.nutrientStore = new Memory();
                    this.nutrientStoreCache = new Cache(nutrientStore, this.nutrientStore);
                },
                startup: function (){
                    this.inherited(arguments);
                    // load cache
                    this.nutrientStoreCache.query({id:""});
                    var filteringSelect = new FilteringSelect({
                        store: this.nutrientStore,
                    }, this.nutrientsSelect);
                    filteringSelect.startup ();
                },
                onSaveFood: function(e){
                    console.log('onSaveFood');
                    var food = e;
                },
                onAddFood: function(e){
                    console.log('onAddFood');
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
