require([
    "dojo/ready", 
    "supplementme/main", 
],
        function (ready) {

                describe("Test creation of main class", function(){
                    it("should have Main availiable in namespace", function(){
                        expect(supplementme.Main().user).toEqual('anonymous');
                        expect(supplementme.Main({'user':'testuser'}).user).toEqual('testuser');
                    });
                });
        });
