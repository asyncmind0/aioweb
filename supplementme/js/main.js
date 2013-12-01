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
             _WidgetsInTemplateMixin, _OnDijitClickMixin], {
                 templateString: food_template,
             });

    declare("supplementme.MealWidget",
            [_WidgetBase, _TemplatedMixin, 
             _WidgetsInTemplateMixin, _OnDijitClickMixin,
             JsonRest, Memory, Cache, Observable
            ], {
                templateString: meal_template,
                constructor: function(args){
                    declare.safeMixin(this, args);
                    masterStore = new JsonRest({
                        target: "/meal/"
                    });
                    cacheStore = new Memory({ });
                    this.mealStore = new Cache(masterStore, cacheStore);
                    debugger;
                    this.mealStore.query({'name':'test'});
                },
                onSaveMeal: function(e){
                    console.log('onSaveMeal');
                    debugger;
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
