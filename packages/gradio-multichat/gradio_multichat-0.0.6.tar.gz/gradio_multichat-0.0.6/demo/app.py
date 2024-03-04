import os
import time
import gradio as gr
from random import choice
from typing import Literal, Optional
from gradio_multichat import MultiChat as mc


def print_like_dislike(x: gr.LikeData):
    print(x.index, x.value, x.liked)


# Setup some custom CSS styles that will be used by some of the characters
css = """
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
"""


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
