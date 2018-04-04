var ws = new SWS('compressor');
		ws.connect();
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