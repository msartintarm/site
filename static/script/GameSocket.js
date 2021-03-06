/**
 * Creates and initializes a websocket to get / send game info.
 */
function GameSocket() {

    var uri = "ws://" + top.location.host + "/socket";
    this.socket = new WebSocket(uri);

    this.socket.onopen = function() {
        console.log("Socket opened.");
    };

    // A message may be a request to append to. or to replace, an existing element.
    // Simple enough .. right?
    // Sometimes, we want a specific callback function.
    this.socket.onmessage = function(e) {

        if (this.callback_fn) {
            this.callback_fn(e);
            this.callback_fn = null;
            return;
        }

        // Convert to DOM structure, and then use DOM manipulation.
        var $result = $("<div></div>").html(e.data);
        if ($result) {
            // Look for replacement element
            var new_element = $result.find(".html-replace");
            var replacement = new_element.attr("data-target");
            if (replacement) {
                var $container = $("#" + replacement);
                var replacer = $container.attr("data-close");
                if (replacer) $("#" + replacer).show().mousedown(function(){
                    $container.html("");
                    $(this).hide();
                });
                $container.html(new_element);

            }
        }
    };

    this.socket.onclose = function() {
        console.log("Socket closed.");
    };

    this.send = function(message, callback) {

        if (callback) this.callback_fn = callback;
        this.socket.send(message);
    }

    // Sets up a button to send a request through the socket.
    this.setupButton = function(button) {
        var sock = this.socket;
        $(button).mousedown(function() {
            console.log("Sending message: " + $(this).data("cmd"));
            sock.send([uri, "/", $(this).data("cmd")].join(""));
        });
    }

    return this;
}
