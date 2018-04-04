
// IP 
var IP = "192.168.43.103:1111";
class SWS{
    constructor(algorithm) {
        this.IP = IP;
        this.algorithm = algorithm;
    }
    connect() {
        var id = location.search.split('id=')[1];
        var string;
        if (id){
            string = '?id='+id}
        else {
            string = ''}
        this.ws = new WebSocket("ws://"+this.IP+"/user/ws"+string);
        this.ws.onopen=function(){

        };
        this.ws.onmessage=function(e){
            var obj = JSON.parse(e.data);
            var func;
            eval('func=' + Object.keys(obj));
            func(obj[Object.keys(obj)]);
        };
        ws.onclose = function() {
        };
    }
    change_onmessage(func){
        this.ws.onmessage = func
    }
    change_onopen(func){
        this.ws.onopen = func
    }
    change_onclose(func){
        this.ws.onclose = func
    }
    send(receiver, val){

        this.ws.send(`{"receiver":"${receiver}", "algorithm":"${this.algorithm}","method":${val}}`)

    }
    disconnect(){
        this.ws.close()
    }
}
































