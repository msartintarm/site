/*
 All text on this page is property of Michael Sartin-Tarm. (c) 2014.
 License is MIT, and in addition, you must give me full notice.

  The purpose of this inline script is to monitor
    whether the WebGL JS has been loaded. 
*/
var the_scene = ""; // global object that is monitored
// cool font animation
(function() {

  var game_sock = new GameSocket();
  game_sock.setupButton("#config-load-button");
  game_sock.setupButton("#about-load-button");

  var i_count = 0;
  var inputz;
  var new_color = parseInt("890abc", 16);
  var limit = parseInt("ffffff", 16);
  var weak_color = parseInt("666666", 16);

  var cool_color = 238 * 256 * 256 + 135 * 256 + 187;

  var started = false;

  var params = window.location.search;
  if(params.length > 1) the_scene = params.substring(1);


  var check_start = function() {
    if (started === true) return true;
    if (the_scene.length > 0) {
      theCanvas.start(the_scene);
      started = true;
    }
    return started;
  };

  window.initGLcanvas = function() {
    if (!GLcanvas || !Game) {
      window.setTimeout(window.initGLcanvas, 50);
    } else if (!theCanvas){
      theCanvas = new GLcanvas();
      window.setTimeout(window.initGLcanvas, 50);
      inputz = document.getElementsByClassName("beginner");
    } else if (!check_start()) {
        window.setTimeout(check_start,  50);
        window.setTimeout(check_start, 100);
        window.setTimeout(window.initGLcanvas, 150);

        var izz = inputz[(++i_count) % inputz.length];
        var new_thing = new_color.toString(16);
        // append leading 0's if needed
        for(var i=new_thing.length; i<6; ++i) new_thing = "0" + new_thing;
        izz.style.color = "#" + new_thing;

        // that should keep things interesting
        new_color = (1487 * (new_color % 557)) * 23 + Math.abs(new_color - cool_color) % limit;
        // color too bright, invert it
        if ((new_color % 256) + (new_color / 256 % 256) + (new_color / (256 * 256) % 256) > 240)
          new_color -= weak_color;
      }

  };
} ());
