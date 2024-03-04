
import gradio as gr
from app import demo as app
import os

_docs = {'MultiChat': {'description': 'Creates a chatbot that displays user-submitted messages and responses. Supports a subset of Markdown including bold, italics, code, tables.\nAlso supports audio/video/image files, which are displayed in the MultiChat, and other kinds of files which are displayed as links. This\ncomponent is usually used as an output component.\n', 'members': {'__init__': {'value': {'type': 'list[dict[str, str | None]] | None', 'default': 'None', 'description': None}, 'characters': {'type': 'list[dict] | None', 'default': 'None', 'description': None}, 'label': {'type': 'str | None', 'default': 'None', 'description': None}, 'every': {'type': 'float | None', 'default': 'None', 'description': None}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label. Defaults to None.'}, 'container': {'type': 'bool', 'default': 'True', 'description': None}, 'scale': {'type': 'int | None', 'default': 'None', 'description': None}, 'min_width': {'type': 'int', 'default': '160', 'description': None}, 'visible': {'type': 'bool', 'default': 'True', 'description': None}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': None}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': None}, 'render': {'type': 'bool', 'default': 'True', 'description': None}, 'height': {'type': 'int | str | None', 'default': 'None', 'description': None}, 'latex_delimiters': {'type': 'list[dict[str, str | bool]] | None', 'default': 'None', 'description': None}, 'rtl': {'type': 'bool', 'default': 'False', 'description': None}, 'show_copy_button': {'type': 'bool', 'default': 'False', 'description': None}, 'sanitize_html': {'type': 'bool', 'default': 'True', 'description': None}, 'render_markdown': {'type': 'bool', 'default': 'True', 'description': None}, 'bubble_full_width': {'type': 'bool', 'default': 'True', 'description': None}, 'line_breaks': {'type': 'bool', 'default': 'True', 'description': None}, 'likeable': {'type': 'bool', 'default': 'False', 'description': None}, 'layout': {'type': '"panel" | "bubble" | None', 'default': 'None', 'description': None}}, 'postprocess': {'value': {'type': 'list[dict[str, str | list | None]] | None', 'description': 'Receives a list of dictionaries containing dictionaries with both "role" and "content" in each, the "role" can be registred in characters, there is a default "user" and "bot" profile in there if its needed.'}}, 'preprocess': {'return': {'type': 'list[\n        dict[str, str | gradio.data_classes.FileData | None]\n    ]\n    | None', 'description': 'A list of dictionaries that contain ready to deploy messages, or None.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the MultiChat changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the MultiChat. Uses event data gradio.SelectData to carry `value` referring to the label of the MultiChat, and `selected` to refer to state of the MultiChat. See EventData documentation on how to use this event data'}, 'like': {'type': None, 'default': None, 'description': 'This listener is triggered when the user likes/dislikes from within the MultiChat. This event has EventData of type gradio.LikeData that carries information, accessible through LikeData.index and LikeData.value. See EventData documentation on how to use this event data.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'MultiChat': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_multichat`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_multichat/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_multichat"></a>  
</div>

A Gradio Chatbot variant for handling multiple characters with customizable profiles, pictures, and CSS. Ideal for diverse tasks like multi-entity conversations and role-playing scenarios.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_multichat
```

## Usage

```python
import os
import time
import gradio as gr
from random import choice
from typing import Literal, Optional
from gradio_multichat import MultiChat as mc


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


# Setup some custom CSS styles that will be used by some of the characters
css = \"\"\"
.char-style-a {
  color: #0e0e0e;
  background: #8084eb;
  font-size: 22px;
  font-weight: 800;
}
.char-style-b {
  color: #10f1f2;
  background: #666666;
}
.char-style-c {
  background: #a42727;
  font-weight: 600;
}
\"\"\"


class MessageControl:
    def __init__(self, characters: Optional[list[dict[str, None]]]) -> None:
        self.characters = []
        self.participants = []
        if characters:
            [self.process_character(**x) for x in characters]

    def process_character(
        self,
        role: str,
        position: Literal["bot", "user"] | None = None,
        avatar: str | None | os.PathLike = None,
        style: str | None = None,
    ):
        position = (
            "bot"
            if not isinstance(position, str) or position not in ["bot", "user"]
            else position
        )
        self.characters.append(
            {
                "role": role,
                "position": position,
                "avatar": avatar,
                "style": style if isinstance(style, str) and style.strip() else None,
            }
        )
        if role not in self.participants:
            self.participants.append(role)
        return (
            gr.update(choices=self.participants),
            gr.update(characters=self.characters),
            gr.update(characters=self.characters),
        )

    def add_message(self, role: str, message: str):
        return {"role": role, "content": message}

    def clear_history(self):
        return None

    def generate(self, value, participants: list[str], history:list[dict]):
        if not participants:
            participants = self.participants
        history = history["messages"]
        history.append({"role":"user", "content":value})
        yield history
        time.sleep(1)
        history.append({"role":"bot", "content":value})
        yield history
        for character in participants:
            history.append({"role":character, "content":""})
            for char in choice(RANDOM_CHAT):
                history[-1]["content"] += char
                time.sleep(0.015)
                yield history


# Characters for this demo
characters = [
    {"role": "user", "position": "user", "avatar": "demo/User.png"},
    {"role": "bot", "position": "bot", "avatar": "demo/Assistant.png"},
    {"role": "Carl", "position": "user", "style": "char-style-b"},
    {"role": "Klaus", "position": "bot", "avatar": "demo/Klaus.png"},
    {
        "role": "Mark",
        "position": "bot",
        "avatar": "demo/Mark.png",
        "style": "char-style-c",
    },
    {
        "role": "John",
        "position": "user",
        "avatar": "demo/John.png",
        "style": "char-style-a",
    },
]
# Random speech lines for testing:
RANDOM_CHAT = [
    "Did you know that pineapples wear sunglasses during winter?",
    "I tried teaching my pet rock algebra, but it kept rolling away.",
    "In a parallel universe, marshmallows are the currency.",
    "My toaster and I have deep philosophical discussions about life.",
    "Yesterday, I saw a giraffe playing the saxophone in the park.",
    "I'm thinking of starting a dance crew for synchronized swimming.",
    "Bananas have secret meetings at midnight to discuss their peelings.",
    "I have a collection of invisible paintings – they're quite rare.",
    "I communicate with my plants through interpretive dance.",
    "I once raced a snail. It was intense, but I lost... eventually.",
    "I speak fluent penguin – it's a highly underrated skill.",
    "I'm training my pet rock to participate in the next rock Olympics.",
    "Have you ever tried square-shaped watermelons? They taste cubic.",
    "I have a conspiracy theory that trees are just really slow dancers.",
]

with gr.Blocks(css=css, title="Demo gradio_multichat") as demo:
    msg = MessageControl(characters)
    msg.history = [
        {"role": "user", "content": choice(RANDOM_CHAT)},
        {"role": "bot", "content": choice(RANDOM_CHAT)},
        {"role": "Mark", "content": choice(RANDOM_CHAT)},
        {"role": "John", "content": choice(RANDOM_CHAT)},
    ]

    chatbot = mc(
        value=msg.history,
        label="MultiChatbot",
        characters=msg.characters,
        layout="bubble",
        height=600,
        likeable=True,
        show_copy_button=True,
    )

    with gr.Row():
        with gr.Column(scale=999):
            text_input = gr.Textbox(
                interactive=True,
                placeholder="Write here your message.",
                container=False,
                lines=7,
                max_lines=7,
            )
        with gr.Group():
            send_button = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear")
            delete_last_btn = gr.Button("Delete Last Entry", variant="stop")
            edit_last_btn = gr.Button("Edit Last Entry")

    with gr.Row():
        chatstyle_menu = gr.Dropdown(
            choices=["bubble", "panel"],
            value="bubble",
            interactive=True,
            label="MultiChat Style",
            allow_custom_value=True,
        )
        participants_menu = gr.Dropdown(
            choices=msg.participants,
            interactive=True,
            label="Participants",
            max_choices=32,
            multiselect=True,
            allow_custom_value=True,
        )
    with gr.Accordion("Create Character"):
        with gr.Row():
            char_name = gr.Textbox(
                interactive=True,
                label="Character's Name",
                placeholder="Insert the character's name here",
            )
            char_position = gr.Dropdown(
                ["user", "bot"],
                value="bot",
                interactive=True,
                label="Character's position",
            )
        with gr.Row():
            char_picture = gr.Textbox(
                interactive=True,
                label="Character Profile Picture (Optional)",
                placeholder="Url or Path to image to be used as profile picture.",
            )
            char_style = gr.Textbox(
                interactive=True,
                label="CSS Style Template (Optional)",
                placeholder="CSS Style here.",
            )
        with gr.Row():
            btn_addchat = gr.Button("Add Character", variant="primary")
            chat_print = gr.Button("Print Content from chat")

    def ccf():
        return None, None, None, None

    btn_addchat.click(
        msg.process_character,
        [char_name, char_position, char_picture, char_style],
        [participants_menu, chatbot],
    ).then(
        ccf,
        outputs=[char_name, char_position, char_picture, char_style],
    )

    chat_print.click(lambda x: print(x), chatbot)
    chatstyle_menu.change(lambda x: gr.update(layout=x), chatstyle_menu, chatbot)
    gr.on(
        [send_button.click, text_input.submit],
        msg.generate,
        [text_input, participants_menu, chatbot],
        [chatbot],
    )

    clear_btn.click(lambda: None, outputs=[chatbot])

    chatbot.like(print_like_dislike, None, None)


if __name__ == "__main__":
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `MultiChat`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["MultiChat"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["MultiChat"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, a list of dictionaries that contain ready to deploy messages, or None.
- **As output:** Should return, receives a list of dictionaries containing dictionaries with both "role" and "content" in each, the "role" can be registred in characters, there is a default "user" and "bot" profile in there if its needed.

 ```python
def predict(
    value: list[
        dict[str, str | gradio.data_classes.FileData | None]
    ]
    | None
) -> list[dict[str, str | list | None]] | None:
    return value
```
""", elem_classes=["md-custom", "MultiChat-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          MultiChat: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
