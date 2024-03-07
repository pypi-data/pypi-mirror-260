import anywidget
import traitlets

def kloudhello(number):
    print("hello from kloud")

class KloudToken(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        console.log("JS Token is", window.kloud_token);
        model.set("value", window.kloud_token || "n/a");
        model.save_changes();
    };
    
    function initialize({ model }) {
        console.log("Initialize kloud token JS", window);
    }
    export default { render };
    """
    _css = ""
    value = traitlets.Unicode("default").tag(sync=True)
