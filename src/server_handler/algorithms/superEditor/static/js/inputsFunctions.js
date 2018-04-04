function animate_plane(){
    object_svg = document.getElementById('animation');
    content = object_svg.contentDocument;
    plane = content.getElementById("airplane");
    front_cloud = content.getElementById("cloud_front");
    back_cloud = content.getElementById("cloud_back");

    x_0_plane=0;
    v_plane = 20;
    interval = setInterval(function(){
        x_0_plane+=v_plane*15/1000;
        plane.setAttribute('transform','translate (-'+x_0_plane+'0)');
        if (x_0_plane>=140){
            clearInterval(interval)
        }
    }, 15);

    x_0_cloud_back = 0;
    x_0_cloud_front = 0;
    v_back=30;
    v_front=40;
    console.log(x_0_plane);
    interval2 = setInterval(function(){
        x_0_cloud_front+=v_front*15/1000;
        front_cloud.setAttribute('transform','translate ('+x_0_cloud_front+'0)');
        x_0_cloud_back+=v_back*15/1000;
        back_cloud.setAttribute('transform','translate ('+x_0_cloud_back+'0)');
        if (x_0_cloud_front>=600){
            clearInterval(interval2)
        }
    }, 15)
}
function show(name) {
    container=document.getElementById('variableScene');
    childs = container.childNodes;
    for(i=0; i < childs.length; i++) {
        if (childs[i].nodeName === 'DIV'){
            childs[i].setAttribute('style', 'display: None');
            if (childs[i].attributes.getNamedItem('id').textContent === name){

                childs[i].setAttribute('style', 'display: block');
            }
        }

    }
}
function show_help(name){
   container=document.getElementById('explication');
    childs = container.childNodes;
    for(i=0; i < childs.length; i++) {
        if (childs[i].nodeName === 'DIV'){
            childs[i].setAttribute('style', 'display: None');
            if (childs[i].attributes.getNamedItem('id').textContent === name){

                childs[i].setAttribute('style', 'display: block');
            }
            if (childs[i].attributes.getNamedItem('id').textContent === 'entrada_help'){
                animate_plane()
            }
        }
    }
}