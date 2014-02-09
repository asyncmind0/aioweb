require([
    "dojo/_base/declare", "dijit/_WidgetBase",
    "dijit/_TemplatedMixin", "dijit/_WidgetsInTemplateMixin",
    "dijit/_OnDijitClickMixin", "dojo/store/JsonRest",
    "dojo/store/Memory", "dojo/store/Cache", "dojo/store/Observable",
    "dojo/ready", "dojo/parser", "dijit/form/Form",
    "dijit/form/FilteringSelect", "dijit/form/TextBox",
    "dijit/form/NumberSpinner", "dijit/form/Select", "dojo/json",
    "dojo/when", "dojo/on", "dojo/dom-construct", "dojo/request",
    "dojo/text!supplementme/mealwidget.html",
], function(declare, _WidgetBase,
            _TemplatedMixin, _WidgetsInTemplateMixin,
            _OnDijitClickMixin, JsonRest, Memory, Cache, Observable,
            ready, parser, Form, FilteringSelect, TextBox,
            NumberSpinner, Select, json, when,on, domConstruct,
            request, meal_template
           ){
    declare("supplementme.MealWidget",
            [_WidgetBase, _TemplatedMixin, 
             _WidgetsInTemplateMixin, _OnDijitClickMixin,
             JsonRest, Memory, Cache, Observable
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
});
