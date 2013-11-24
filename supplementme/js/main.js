require([
    "dojo/_base/declare",
    "dijit/_WidgetBase", "dijit/_TemplatedMixin",
    "dijit/_WidgetsInTemplateMixin",
    "dojo/ready", "dojo/parser", "dijit/form/Form",
    "dojo/text!supplementme/foodwidget.html", 
    "dojo/text!supplementme/mealwidget.html", 
], function(declare, _WidgetBase,
            _TemplatedMixin, _WidgetsInTemplateMixin,
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
            [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        templateString: food_template,
    });
    declare("supplementme.MealWidget",
            [_WidgetBase, _TemplatedMixin, _WidgetsInTemplateMixin], {
        templateString: meal_template,
    });
    ready(function(){
        parser.parse();
    });
});
