require([
    "dojo/ready", 
    "dojo/_base/declare",
    "supplementme/main", 
    "supplementme/test",
], function (ready, declare) {
    declare("supplementme.TestMain_test", supplementme.test, {
        constructor: function(args){
            declare.safeMixin(this, args);
            this.suite = "food widget tests";
        },
        setUp: function(){
            },
        "should have Main availiable in namespace": function(){
            doh.assertTrue(supplementme.Main().user == 'anonymous');
            doh.assertTrue(supplementme.Main({'user':'testuser'}).user == 'testuser');
        }
    });
    ready(function () {
        var testsuite = new supplementme.TestMain_test();
        testsuite.registerTests();
        doh.run();
    });
});
