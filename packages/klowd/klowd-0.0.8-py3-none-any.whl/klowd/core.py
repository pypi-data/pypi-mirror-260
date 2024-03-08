import anywidget
import traitlets

class GrantToken(anywidget.AnyWidget):
    _esm = """\
    function render({ model, el }) {
      const container = document.createElement("div");
      container.classList.add("kloud-confirm-container");
    
      const questionDiv = document.createElement("div");
      questionDiv.innerHTML = 'Скрипт запрашивает доступ к платформе. Разрешить?';
      questionDiv.classList.add("kloud-confirm-question");
      
      const okButton = document.createElement("button");
      okButton.classList.add("kloud-confirm-button");
      okButton.innerHTML = 'Разрешить';
      okButton.addEventListener("click", () => {
        model.set("value", sessionStorage.getItem('kloud_token'));
        model.save_changes();
      });
      container.appendChild(questionDiv);
      container.appendChild(okButton);
      el.appendChild(container);
    }
	export default { render };
    """
    _css = """\
        .kloud-confirm-container {
            align-items: center;
            border: 5px solid var(--jp-rendermime-error-background);
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            font-size: 20px;
            gap: 20px;
            padding: 20px;
        }
        .kloud-confirm-question {
            color: var(--jp-content-font-color1);
            opacity: 0.9;
        }
        
        .kloud-confirm-button {
            background: red;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-size: 20px;
            opacity: 0.8;
            padding: 10px 20px;
        }
    """
    value = traitlets.Unicode("").tag(sync=True)

kloud_token = GrantToken()

def setToken(event):
    kloud_token.close()

kloud_token.observe(setToken, 'value')
kloud_token
