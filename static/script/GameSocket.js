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
    this.socket.onmessage = function(e) {

        // Convert to DOM structure, and then use DOM manipulation.
        var $result = $("<div></div>");
        $result.html(e.data);
        if ($result) {
            // Look for replacement element
            var new_element = $result.find(".html-replace");
            var replacement = new_element.attr("data-id");
            if (replacement) $("#" + replacement).html(new_element);
        }
        else console.log("Message received: " + e.data);
    };

    this.socket.onclose = function() {
        console.log("Socket closed.");
    };

    this.send = function(message, callback) {

        this.socket.send(message);
    }

    // Sets up a button to send a request through the socket.
    this.setupButton = function(button) {
        var sock = this.socket;
        $(button).mousedown(function() {
            console.log("Sending message: " + $(this).data("cmd"));
            sock.send([uri, "/", $(this).data("cmd")].join(""));
        })
    }

    return this;
}
