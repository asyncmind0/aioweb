from db.model import Model

class Nutrient(Model):
    required_fields = ['quantity', 'name']
    views = {
        'keys':{
            'map':"""
                function(doc) {
                    if(doc.doc_type == 'Nutrient' && doc.name) {
                        emit(doc.name, null);
                    }
                }
            """,
            'reduce':"""
                function(keys, values){
                    return true;
                }
            """
        }
    }
    
class Food(Model):
    required_fields = ['name', 'nutrients', 'quantity']