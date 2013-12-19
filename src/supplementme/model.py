from db.model import Model


class Nutrient(Model):
    required_fields = ['name', 'tag', 'unit', 'number', 'decimal_places']
    views = {
        'keys': {
            'map': """
                function(doc) {
                    if(doc.doc_type == 'Nutrient' && doc.name) {
                        emit(doc.name, null);
                    }
                }
            """,
            'reduce': """
                function(keys, values){
                    return true;
                }
            """
        },
        'by_tag': {
            'map': """
                function(doc) {
                    if(doc.doc_type == 'Nutrient' && doc.tag) {
                        emit(doc.tag, null);
                    }
                }
            """,
            'reduce': """
                function(keys, values){
                    return true;
                }
            """
        }

    }


class Food(Model):
    required_fields = ['name', 'nutrients', 'serving_size', 'unit']
    views = {
        'by_name': {
            'map': """
                function(doc) {
                    if(doc.doc_type == 'Food' && doc.name) {
                        emit(doc.name, null);
                    }
                }
            """,
            'reduce': """
                function(keys, values){
                    return true;
                }
            """
        },
        'by_nutrition': {
            'map': """
                function(doc) {
                    if(doc.doc_type == 'Food' && doc.nutrition) {
                        for(n in nutrition){
                            emit(nutrition[n].name, null);
                        }
                    }
                }
            """
        }
    }


class Meal(Model):
    required_fields = ['foods', 'quantity', 'user']
    views = {
        'by_user': {
            'map': """
                function(doc) {
                    if(doc.doc_type == 'Meal' && doc.user) {
                        emit(doc.user, doc);
                    }
                }
            """,
            'reduce': """
                function(keys, values){
                    return true;
                }
            """
        },
    }
