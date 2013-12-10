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
                    var nutrienStore = new JsonRest({
                        target: "/nutrients/"
                    });
                    this.nutrientStore = new Cache(nutrientStore, new Memory({}));
                },
                onSaveFood: function(e){
                    console.log('onSaveFood');
                    var food = e;
                },
                onAddFood: function(e){
                    console.log('onAddFood')
                    food =
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
                    console.log('onAddMeal')
                }
            });
    ready(function(){
        parser.parse();
    });
});
