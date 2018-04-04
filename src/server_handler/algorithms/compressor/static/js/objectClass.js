
class Blade{
    constructor(mesh, pos_init) {
        this.mesh = mesh;
        this.pos_init = pos_init;
        this.current_x = pos_init;
        this.camber=[];
        this.stagger=[];
        this.stations=[];
    }
}

class Compressor{
    constructor(stages, rs, camera){
        this.stages = stages;
        this.blades = [];
        this.meshes = [];
        this.rs = rs;
        this.pos_0 = [];
        this.camera = camera;
        this.meshes = [];
    }
    set_z(blade, z_list){
        this.blades[blade].stations=z_list
    }
    set_camber(blade, camber_list){
        this.blades[blade].camber=camber_list
    }
    set_stagger(blade, stagger_list){
        this.blades[blade].stagger=stagger_list
    }
    paint_graphic(index_obj){

    }
    add_blade(mesh, pos_0){
        this.blades.push(new Blade(mesh, pos_0));
        this.meshes.push(mesh)
    }
    centerBlade(index){

        for (i=0; i<this.blades.length; i++){
            if (i<index){
                this.getOutBlade(i, -5, 10)
            }else if(i>index){
                this.getOutBlade(i, 105, 20)
            }
            else if(i===parseInt(index)){
                this.getOutBlade(i, 3, 5)
            }
        }

        this.fitBlade(index);
        this.current_index = index

    }
    getOutBlade(index, new_x, velocidad){
        var x_0 = this.blades[index].current_x;
        console.log(x_0);
        var vel = new_x - x_0;
        if (vel<=0){
            velocidad = velocidad*-1
        }else if(vel>0){

        }
        var interval=setInterval(function (blade) {
            x_0+=velocidad*15/1000;
            coords = relative_coord(x_0,0);
            blade.mesh.position.set(coords[0], coords[1], coords[2]);
            if (velocidad<0){
                if (new_x>x_0){
                    blade.current_x= new_x;
                    clearInterval(interval)
                }
            }else if (velocidad>0){
                if (x_0>new_x){
                    blade.current_x= new_x;
                    clearInterval(interval)
                }
            }
        }, 15, this.blades[index])
    }
    fitBlade(index){

        var scale_end = (1-0.01)*h_w*widht/this.rs;
        var top_0 = this.rs*0.01;
        var scale_0 = 0.01;
        var velocity = 0.001;
        var interval = setInterval(function (blade) {
            scale_0+=velocity*15/1000;
            if (scale_0>=scale_end){
                clearInterval(interval)
            }
            blade.mesh.scale.set(scale_0,scale_0,scale_0);


        }, 15, this.blades[index]);
        var velocity2 = 1;
        var interval2 = setInterval(function (camera) {

            top_0 += velocity2*15/1000;
            if(top_0>=h_w*widht){
                clearInterval(interval2)
            }
            this.camera.top = top_0;
            this.camera.bottom = top_0 - h_w*widht;
            this.camera.updateProjectionMatrix()
        }, 15, camera)
    }
    showAll(){
        var index = this.current_index;
        for (i=0; i<this.blades.length; i++){
            if (i<index){
                this.getOutBlade(i, this.blades[i].pos_init, 10);
            }else if(i>index){
                this.getOutBlade(i, this.blades[i].pos_init, 20);
            }
            else if(i===index){
                this.getOutBlade(i, this.blades[i].pos_init, 5);
            }
        }
        var scale_end = 0.01;
        var scale_0 = this.blades[index].mesh.scale.x;
        var velocity = 0.004;
        var interval = setInterval(function (blade) {
            scale_0-=velocity*15/1000;
            if (scale_0<=scale_end){
                clearInterval(interval)
            }
            blade.mesh.scale.set(scale_0,scale_0,scale_0);


        }, 15, this.blades[index]);
        var top_0 = this.camera.top;
        var rs = this.rs*0.01;
        var velocity3 = 1;
        var interval65 = setInterval(function () {
            top_0 -= velocity3*15/1000;
            if(top_0<= rs){
                clearInterval(interval65)
            }
            console.log(top_0, rs);
            this.camera.top = top_0;
            this.camera.bottom = top_0 - h_w*widht;
            this.camera.updateProjectionMatrix();
        }, 15)

    }

}