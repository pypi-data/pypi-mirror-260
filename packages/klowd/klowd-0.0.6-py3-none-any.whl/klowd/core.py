import anywidget
import traitlets

def kloudhello(number):
    print("hello from kloud")

class KloudToken(anywidget.AnyWidget):
    _esm = """
    function render({ model, el }) {
        model.set(\"value\", window.kloud_token || \"n/a\");
        model.save_changes();
    };
    export default { render };
    """
    _css = ""
    value = traitlets.Unicode("default").tag(sync=True)
