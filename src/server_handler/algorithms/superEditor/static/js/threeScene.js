if ( ! Detector.webgl ) Detector.addGetWebGLMessage();
		var container;
		var mouse = new THREE.Vector2(), INTERSECTED, INTERSECTING;
		var camera, cameraTarget, scene, renderer;
		var meshes;
		var mesh;
		var compressor, planes;
		var raycaster;
		var widht=10;
		var h_w=0.95*0.98*window.innerHeight/(0.75*window.innerWidth);
		init();
		animate();
		function init() {
			container = document.getElementById('results_scene');
			camera = new THREE.OrthographicCamera(0, widht, 4.3, 4.3-h_w*widht, 2, 10);
			camera.position.set( 0, 0, 5 );
			cameraTarget = new THREE.Vector3( 0, 0, 0 );
			scene = new THREE.Scene();
			scene.background = new THREE.Color( 0xB4B4B4 );
			//scene.fog = new THREE.Fog( 0x72645b, 2, 15 );
			// Ground
			var plane = new THREE.Mesh(
				new THREE.PlaneBufferGeometry( 40, 40 ),
				new THREE.MeshPhongMaterial( { color: 0x999999, specular: 0x101010 } )
			);
			plane.rotation.x = -Math.PI/2;
			plane.position.y = -0.5;
			plane.position.z = 23;
			//scene.add( plane );
			plane.receiveShadow = true;
			//sky Dome
			var skyGeo = new THREE.SphereGeometry(1, 25, 25);
			var texture_loader = new THREE.TextureLoader();
			var texture=texture_loader.load("/algorithms/compressor/static/texture2.jpg");
			var material = new THREE.MeshPhongMaterial({
					map: texture
			});
			var sky = new THREE.Mesh(skyGeo, material);
			sky.position.set(2,h_w*widht,0);
			sky.material.side = THREE.FrontSide;
			//scene.add(sky);
			// env map
			var path = "/algorithms/compressor/static/SwedishRoyalCastle/";
			var format = '.jpg';
			var urls = [
					path + 'px' + format, path + 'nx' + format,
					path + 'py' + format, path + 'ny' + format,
					path + 'pz' + format, path + 'nz' + format
				];
			var reflectionCube = new THREE.CubeTextureLoader().load( urls );
			// material

			// load STL
			stages = 10;
			var loader = new THREE.STLLoader();
			meshes = [];
			compressor = new Compressor(stages, 430, camera);

			function add_stl(name, pos){
				loader.load( name, function ( geometry ) {
			    var material = new THREE.MeshStandardMaterial( {
				color: 0x888888,
				roughness: 0.4,
				metalness: 1,
				envMap: reflectionCube,
				envMapIntensity: 1,
				side: THREE.DoubleSide
			} );
				var mesh = new THREE.Mesh( geometry, material );
				step = 100/(stages*2);
				coords = relative_coord(4+step*pos,0);
				mesh.name = pos;
				mesh.position.set(coords[0], coords[1], coords[2]);
				mesh.rotation.set( -Math.PI/2, 0, 0 );
				mesh.scale.set( 0.01, 0.01, 0.01 );
				mesh.castShadow = true;
				mesh.receiveShadow = true;
				scene.add( mesh );
				compressor.add_blade(mesh,4+step*pos);
			} );
			}
			add_stl('/algorithms/compressor/static/R_1.stl', 0);
			add_stl('/algorithms/compressor/static/R_2.stl', 1);
			add_stl('/algorithms/compressor/static/R_3.stl', 2);
			add_stl('/algorithms/compressor/static/R_4.stl', 3);
			INTERSECTING = compressor.meshes;

			// Lights
			scene.add( new THREE.HemisphereLight( 0x6E6E6E, 0x111122 ) );

			// renderer
			renderer = new THREE.WebGLRenderer( { antialias: true } );
			renderer.setPixelRatio( window.devicePixelRatio );
			renderer.setSize( window.innerWidth, window.innerHeight );
			renderer.gammaInput = true;
			renderer.gammaOutput = true;
			renderer.shadowMap.enabled = true;
			renderer.shadowMap.renderReverseSided = false;
			renderer.domElement.setAttribute('style', 'z-index: 0; width:100%; height:100%;');
			container.appendChild( renderer.domElement );

			// Raycaster
			raycaster = new THREE.Raycaster(); // create once
			mouse = new THREE.Vector2(); // create once

			container.addEventListener( 'mousemove', onDocumentMouseMove, false );
			container.addEventListener('click', onClick);
			container.addEventListener('dblclick', dblClick)
		}
		function dblClick() {
			compressor.showAll();
			INTERSECTING = compressor.meshes
        }
        function setStreamlines(n){
		    planes = [];
		    for (i=0; i<n;i++){
		        var geometry = new THREE.BoxBufferGeometry( 1, 0.05, 0.2 );
				var object = new THREE.Mesh( geometry, new THREE.MeshLambertMaterial( { color: 0xFAFAD2 } ) );
				object.visible = false;
				planes.push(object)
			}
		}
		setStreamlines(6);
		function onClick (event) {
		    raycaster.setFromCamera( mouse, camera );
			var intersects = raycaster.intersectObjects( compressor.meshes , true);
			if (intersects.length>=0) {
			    index_obj = intersects[0].object.name;
			    compressor.centerBlade(index_obj, h_w*widht);
			    }
			INTERSECTING = planes;
			scene.add(object);
		}
		function onDocumentMouseMove( event ) {
				event.preventDefault();
				mouse.x = ( (event.clientX-$('#results_scene').offset().left) / $("#results_scene").width() ) * 2 - 1;
				mouse.y = - ( (event.clientY-$('#results_scene').offset().top) / $("#results_scene").height() ) * 2 + 1;
			}
		function addShadowedLight( x, y, z, color, intensity ) {
			var directionalLight = new THREE.DirectionalLight( color, intensity );
			directionalLight.position.set( x, y, z );
			scene.add( directionalLight );
			directionalLight.castShadow = true;
			var d = 1;
			directionalLight.shadow.camera.left = -d;
			directionalLight.shadow.camera.right = d;
			directionalLight.shadow.camera.top = d;
			directionalLight.shadow.camera.bottom = -d;
			directionalLight.shadow.camera.near = 1;
			directionalLight.shadow.camera.far = 4;
			directionalLight.shadow.mapSize.width = 1024;
			directionalLight.shadow.mapSize.height = 1024;
			directionalLight.shadow.bias = -0.005;
		}
		function animate() {
			requestAnimationFrame( animate );
			render();
		}
		function render() {

		    // find intersections
				raycaster.setFromCamera( mouse, camera );
				var intersects = raycaster.intersectObjects( INTERSECTING , true);
				if (intersects.length>0){
				    if ( INTERSECTED != intersects[ 0 ].object ) {
						if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
						INTERSECTED = intersects[ 0 ].object;
						INTERSECTED.currentHex = INTERSECTED.material.emissive.getHex();
						INTERSECTED.material.emissive.setHex( 0xff0000 );
					}
				} else {
					if ( INTERSECTED ) INTERSECTED.material.emissive.setHex( INTERSECTED.currentHex );
					INTERSECTED = null;
				}

			camera.lookAt( cameraTarget );
			renderer.render( scene, camera );
		}
		function relative_coord(coord_x,coord_y){
			// en %
			new_coor_x = coord_x*widht/100;
			new_coor_y = coord_y*widht*h_w/100;
			return [new_coor_x, new_coor_y, 0]
		}