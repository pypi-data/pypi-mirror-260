import anywidget
import traitlets
import pathlib

def kloudhello(number):
    print("hello from kloud")

class KloudToken(anywidget.AnyWidget):
    _esm = "function render({ model, el }) { model.set(\"value\", window.kloud_token); model.save_changes(); }; export default { render };"
    _css = ""
    token = traitlets.Unicode('').tag(sync=True)
