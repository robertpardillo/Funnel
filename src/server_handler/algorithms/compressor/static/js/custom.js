$(".btn_collapse").on("click", function(){
    var parent = this;
    clicked = parent.getAttribute('clicked');
    console.log(clicked);
    if(clicked==="true"){
        collapse_button(parent);
        parent.setAttribute('clicked', false);
        console.log('collapse')
    } else{
        expand_button(parent);
        parent.setAttribute('clicked', true);
        console.log('expand')
    }


});

function expand_button(parent){
    target = $(parent.getAttribute('data-target'));
    target.css('display', 'block');
    time = 500; //ms
    incre_widht = 20;
    ratio = 500/15;
    ratio2 = 20/ratio;
    current_widht = 0;
    var interval = setInterval(function (){
        current_widht += ratio2;
        parent.setAttribute('style','left:'+(current_widht+1)+'%');
        target.css('width', current_widht+'%');
        if (current_widht>=20){
            clearInterval(interval)
        }
    }, 15);
}

function collapse_button(parent){
    target = $(parent.getAttribute('data-target'));
    target.css('display', 'block');
    time = 500; //ms
    incre_widht = 20;
    ratio = 500/15;
    ratio2 = incre_widht/ratio;
    current_widht = 20;
    var interval = setInterval(function (){
        current_widht -= ratio2;
        parent.setAttribute('style','left:'+(current_widht+1)+'%');
        target.css('width', current_widht+'%');
        if (current_widht<=0){
            target.css('display', 'none');
            clearInterval(interval)
        }
    }, 15);
}