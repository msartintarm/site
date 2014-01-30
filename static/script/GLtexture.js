var textures_loading = 0;

function GLtexture(gl_, index_, image_name) {

    if(typeof gl_.tex_enum[index_] != 'undefined') return;
    gl_.tex_enum[index_] = -1;
    textures_loading ++;

    // REMOVED: Use base64 encoding to keep image client-side
    // NEW: Just fetch the picture and paste it to canvas.
    this.img = new Image();

    this.img.src = "/textures/" + image_name;

    this.active = (++gl_.active);

    this.sampler = (++theCanvas.shader["default"].sampler);
    gl_.tex_enum[index_] = this.active;

    this.img.onload = this.init.bind(this, gl_, index_);

    this.img.onerror = function(){ alert("problem with texture " +
					 index_ + " active: " + this.active); };
    return this;
}

GLtexture.prototype.init = function(gl_,
				    index_,
				    status) {

    var the_texture = gl_.createTexture();

    gl_.activeTexture(gl_.TEXTURE0 + this.active);
    gl_.bindTexture(gl_.TEXTURE_2D, the_texture);
    gl_.texImage2D(gl_.TEXTURE_2D, 0,
		   gl_.RGBA, gl_.RGBA,
		   gl_.UNSIGNED_BYTE, this.img);
    if(index_ !== SKYBOX_TEXTURE_REAL){
	gl_.texParameteri(gl_.TEXTURE_2D,
			  gl_.TEXTURE_MAG_FILTER,
			  gl_.LINEAR);
	gl_.texParameteri(gl_.TEXTURE_2D,
			  gl_.TEXTURE_MIN_FILTER,
			  gl_.LINEAR_MIPMAP_NEAREST);
    } else{
	gl_.texParameteri(gl_.TEXTURE_2D,
			  gl_.TEXTURE_WRAP_S,
			  gl_.CLAMP_TO_EDGE);
	gl_.texParameteri(gl_.TEXTURE_2D,
			  gl_.TEXTURE_WRAP_T,
			  gl_.CLAMP_TO_EDGE);
    }
    gl_.generateMipmap(gl_.TEXTURE_2D);

    console.log("tex: [" + this.active + "," + this.sampler + "," + index_ + "]");

    if((--textures_loading) === 0) {
	console.log("all textures loaded.");
	theCanvas.done_loading(1500);
    }
};

/**
 * Extracts EXIF data describing the conditions under
 *  which this picture was taken.
 * Code borrowed from http://www.nihilogic.dk/labs/exif/exif.js,
 *  licensed under MPL 1.1
 * TODO
 */
GLtexture.prototype.getData = function() {};

GLtexture.create = function (gl_, num, name) {
    var x = new GLtexture(gl_, num, name);
}

GLtexture.fromImage = function (gl_, name) {

}