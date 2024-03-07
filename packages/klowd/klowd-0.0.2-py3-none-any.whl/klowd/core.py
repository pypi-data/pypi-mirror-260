import anywidget
import traitlets
import pathlib

def kloudhello(number):
    print("hello from kloud")

class KloudToken(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "widget.js"
    _css = "function render({ model, el }) { model.set(\"value\", window.kloud_token); model.save_changes(); }; export default { render };"
    token = traitlets.Unicode('').tag(sync=True)
