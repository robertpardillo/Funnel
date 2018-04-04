var ws = new SWS('compressor');

ws.connect();
ws.change_onopen(function () {
    ws.send('handler',`{"get_id":[]}`)
});
document.getElementById('inputs_scene').addEventListener('keyup', input_enter);
function input_enter(e) {
    if (e.keyCode == 13) {
        send_information();
    }

}

function send_information() {
    mach=$('#input_mach').val();
    p=$('#input_p').val();
    t=$('#input_t').val();
    mass=$('#input_mass_flow').val();
    pi=$('#input_compr_ratio').val();
    size=$('#input_size').val();
    stall=$('#input_stall').val();
    cost=$('#input_cost').val();
    off_design=$('#input_off_design').val();
    streamlines=$('#input_streamlines').val();
    method=$('#input_method').val();
    mesh=$('#input_mesh').val();
    ws.send('design', `{"init_analysis": [${mach}, ${p}, ${t}, ${mass}, ${pi}, [${size},${stall},${cost},${off_design}],${streamlines},"${method}",${mesh}]}`)
    ws.send('CFD', `{"simulation_params": ["${method}",${mesh}]}`)
}
var _id;
function set_id(val) {
    _id=val;
    $('#id_').text(val)
}
var z_list;

function set_z(val) {
    z_list = val[1];
    blade=val[0];
    for (var i = 0; i<planes.length; i++) {

        coords = relative_coord(8, val[1][i]*100/0.54);

        planes[i].position.set(coords[0], coords[1], coords[2])
    }
    compressor.set_z(val[0], val[1])
}

function set_camber(val) {
    var x = [];
    for (var i=0; i<val[0].length; i++) {
        x.push(val[0][i])
    }
    var trace1 = {
        x: x,
        y: val[2],
        type: 'scatter',
        name:"profile"
        };
    var x = [];
    for (var i=0; i<val[0].length; i++) {
        x.push(val[1][i])
    }
    var trace2 = {
        x: x,
        y: val[2],
        type: 'scatter',
        name: 'stagger angle'
        };

    var data = [trace1, trace2];
    div = document.getElementById('camber_graf');
    Plotly.newPlot(div, data)
}

function enable_blade(val){
    download_button = document.getElementById('download_button');
    download_button.setAttribute('href','get_from_other/'+val);
    path = 'get_from_other/'+val;
    name='';
    for (i=path.length-1; i>0; i--){
        if (path[i]==='/'){
            break
        }
        console.log(path[i])
        name+=path[i];
    }
    console.log(name);
    name = reverseString(name);
    console.log(name);
    download_button.setAttribute('download', name);

    _add_stl('get_from_other/'+val);
}
function reverseString(str) {
    // Step 1. Use the split() method to return a new array
    var splitString = str.split(""); // var splitString = "hello".split("");
    // ["h", "e", "l", "l", "o"]

    // Step 2. Use the reverse() method to reverse the new created array
    var reverseArray = splitString.reverse(); // var reverseArray = ["h", "e", "l", "l", "o"].reverse();
    // ["o", "l", "l", "e", "h"]

    // Step 3. Use the join() method to join all elements of the array into a string
    var joinArray = reverseArray.join(""); // var joinArray = ["o", "l", "l", "e", "h"].join("");
    // "olleh"

    //Step 4. Return the reversed string
    return joinArray; // "olleh"
}