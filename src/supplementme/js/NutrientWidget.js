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
    "supplementme/NutrientWidget",
    "dojo/text!supplementme/nutrientwidget.html", 
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
            NutrientWidget,
            nutrient_template
           ){
    declare("supplementme.NutrientWidget",
            [_WidgetBase, _TemplatedMixin, 
             _WidgetsInTemplateMixin, _OnDijitClickMixin,
             JsonRest, Memory, Cache, Observable
            ], {
                templateString: nutrient_template,
                constructor: function(args){
                    this.foodNutrients = {};
                    declare.safeMixin(this, args);
                    var nutrientStore = new JsonRest({
                        target: "/nutrients/",
                    });
                    this.nutrientStore = new Memory();
                    this.nutrientStoreCache = new Cache(nutrientStore, this.nutrientStore);
                    this.nutrientStoreCache.query({id:""});
                    on.emit(this, "ready", {
                        bubbles: true,
                        cancelable: false
                    });
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
                    this.nutrientFilteringSelect.startup ();
                },
                reset: function(){
                    this.nutrientFilteringSelect.reset();
                },
                getData: function(){
                    var value = this.nutrientFilteringSelect.get('value');
                    var label = this.nutrientFilteringSelect.get('displayedValue');
                    var qty = this.nutrientQuantity.get('value');
                    var unit = this.nutrientUnit.get('value');
                    return {value:value, label:label, quantity:qty, unit:unit};
                },
                _onAddNutrient: function(e){
                    var data = this.getData();
                    if(!data.value || dojo.indexOf(this.foodNutrients, data.value) >= 0){return;}
                    this.reset();
                    this.foodNutrients[data.value]={quantity:data.quantity, unit:data.unit};
                    on.emit(this, "AddNutrient", {
                        bubbles: true,
                        cancelable: false,
                        data: data
                    });
                },
                onAddNutrient: function(data){
                }
           });
});

