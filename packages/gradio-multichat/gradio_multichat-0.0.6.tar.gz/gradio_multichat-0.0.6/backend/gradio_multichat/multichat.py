"""A variant of Gradio's Chatbot component that can handle multiple characters, each of which can be customized with a profile picture, custom CSS template."""

from __future__ import annotations

import inspect
from typing import Any, Dict, List, Literal, Optional, Tuple, Union
import logging
from gradio_client import utils as client_utils
from gradio import Blocks
from gradio import processing_utils, utils
from gradio.components.base import Component
from gradio.data_classes import FileData, GradioModel, GradioRootModel
from gradio.events import Events
from enum import Enum
import json


class RoleEnum(str, Enum):
    bot = "bot"
    user = "user"


class FileMessage(GradioModel):
    file: FileData
    alt_text: Optional[str] = None


class ChatbotData(GradioRootModel):
    root: List[Dict[Any, Any]]


class MultiChat(Component):
    """
    Creates a chatbot that displays user-submitted messages and responses. Supports a subset of Markdown including bold, italics, code, tables.
    Also supports audio/video/image files, which are displayed in the MultiChat, and other kinds of files which are displayed as links. This
    component is usually used as an output component.

    Demos: chatbot_simple, chatbot_multimodal
    Guides: creating-a-chatbot
    """

    EVENTS = [Events.change, Events.select, Events.like]
    data_model = ChatbotData

    def __init__(
        self,
        value: list[dict[str, str | None]] | None = None,
        *,
        characters: list[dict] | None = None,
        label: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        height: int | str | None = None,
        latex_delimiters: list[dict[str, str | bool]] | None = None,
        rtl: bool = False,
        show_copy_button: bool = False,
        sanitize_html: bool = True,
        render_markdown: bool = True,
        bubble_full_width: bool = True,
        line_breaks: bool = True,
        likeable: bool = False,
        layout: Literal["panel", "bubble"] | None = None,
    ):
        """
        Args:
            value (list[dict[str, str  |  None]] | None, optional): Default value to show in chatbot. If callable, the function will be called whenever the app loads to set the initial value of the component. Format: [{"role":"Name of the character/agent", "content":"The usual contents of a message here"}]. Defaults to None.
            characters (list[dict] | None, optional): A list designed for assigning profile images and custom styles to individual characters within a conversation. Each character is represented by a dictionary with the following format: [{"role": The "character's assigned name.", "position": "Indicated as either 'bot' or 'user', determining the character's placement in the conversation.", "avatar": An optional entry for a custom avatar, specified by either a file path or a URL.", "style": "An optional entry that should point towards the CCS style desired for the character. The CSS Style must be assigned in the Gradio Block's inicialization, like this 'Blocks(css=your_css_string)'."}]
            label (str | None, optional): The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to. Defaults to None.
            every (float | None, optional): If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label. Defaults to None.
            container (bool, optional): If True, will place the component in a container - providing some extra padding around the border. Defaults to True.
            scale (int | None, optional):  relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True. Defaults to None.
            min_width (int, optional): minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first. Defaults to 160.
            visible (bool, optional): If False, component will be hidden. Defaults to True.
            elem_id (str | None, optional): An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles. Defaults to None.
            elem_classes (list[str] | str | None, optional): An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles. Defaults to None.
            render (bool, optional): If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later. Defaults to True.
            height (int | str | None, optional): The height of the component, specified in pixels if a number is passed, or in CSS units if a string is passed. Defaults to None.
            latex_delimiters (list[dict[str, str  |  bool]] | None, optional): A list of dicts of the form {"left": open delimiter (str), "right": close delimiter (str), "display": whether to display in newline (bool)} that will be used to render LaTeX expressions. If not provided, `latex_delimiters` is set to `[{ "left": "$$", "right": "$$", "display": True }]`, so only expressions enclosed in $$ delimiters will be rendered as LaTeX, and in a new line. Pass in an empty list to disable LaTeX rendering. For more information, see the [KaTeX documentation](https://katex.org/docs/autorender.html). Defaults to None.
            rtl (bool, optional): If True, sets the direction of the rendered text to right-to-left. Default is False, which renders text left-to-right. Defaults to false.
            show_copy_button (bool, optional): If True, will show a copy button for each chatbot message. Defaults to False.
            sanitize_html (bool, optional): If False, will disable HTML sanitization for chatbot messages. This is not recommended, as it can lead to security vulnerabilities. Defaults to True.
            render_markdown (bool, optional): If False, will disable Markdown rendering for chatbot messages. Defaults to True.
            bubble_full_width (bool, optional): If False, the chat bubble will fit to the content of the message. If True (default), the chat bubble will be the full width of the component. Defaults to True.
            line_breaks (bool, optional): If True, will enable Github-flavored Markdown line breaks in chatbot messages. If False, single new lines will be ignored. Only applies if `render_markdown` is True. Defaults to True.
            likeable (bool, optional): Whether the chat messages display a like or dislike button. Set automatically by the .like method but has to be present in the signature for it to show up in the config. Defaults to False.
            layout (Literal[&quot;panel&quot;, &quot;bubble&quot;] | None, optional): If "panel", will display the chatbot in a llm style layout. If "bubble", will display the chatbot with message bubbles, with the user and bot messages on alterating sides. Defaults to None (bubble).
        """
        self.likeable = likeable
        self.height = height
        self.rtl = rtl
        if latex_delimiters is None:
            latex_delimiters = [{"left": "$$", "right": "$$", "display": True}]
        self.latex_delimiters = latex_delimiters
        self.render_markdown = render_markdown
        self.show_copy_button = show_copy_button
        self.sanitize_html = sanitize_html
        self.bubble_full_width = bubble_full_width
        self.line_breaks = line_breaks
        self.layout = layout
        self.characters = characters
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            render=render,
            value=value,
        )
        self._load_characters(self.characters)

    def _load_characters(self, characters: list[dict, str | None] = []):

        if not hasattr(self, "registred_characters"):
            self.registred_characters = {
                "user": {"position": "user", "avatar": None, "style": None},
                "bot": {"position": "bot", "avatar": None, "style": None},
            }
        if isinstance(characters, list) and characters:

            for character in characters:
                if isinstance(character, dict):
                    name = character.get("role")
                    position = character.get("position")
                    if not isinstance(name, str) or not name.strip():
                        raise ValueError(
                            "Invalid role, role must be a non-empty string!"
                        )
                    if isinstance(position, str):
                        position = position.strip().lower()
                        if position not in ["user", "bot"]:
                            logging.log(
                                logging.WARNING,
                                f"'{position}' Is not a valid position! It must be either 'user' or 'bot'.",
                                "Using 'None' Instead!",
                            )
                            position = None

                    else:
                        # Ensure that its None value if is not a string
                        position = None

                    self.registred_characters.update(
                        {
                            name: {
                                "position": position,
                                "avatar": Blocks.move_resource_to_block_cache(
                                    self, character.get("avatar")
                                ),
                                "style": character.get("style"),
                            }
                        }
                    )

        self.characters = []

    def _preprocess_message(
        self, contents: FileMessage | None
    ) -> Optional[Union[str | FileMessage]]:
        if not hasattr(self, "registred_characters"):
            self._load_characters()
        if isinstance(contents, FileMessage):
            if contents.alt_text:
                return (contents.file.path, contents.alt_text)
            else:
                return (contents.file.path, None)
        elif isinstance(contents, str):
            return contents
        else:
            return None

    def preprocess(
        self,
        payload: ChatbotData | list[dict] | None,  # ChatbotData
    ) -> list[dict[str, str | FileData | None]] | None:
        """
        Parameters:
            payload: Receives a list of dictionaries containing dictionaries with both \"role\" and \"content\" in each, the \"role\" can be registred in characters, there is a default \"user\" and \"bot\" profile in there if its needed.
        Returns:
            A list of dictionaries that contain ready to deploy messages, or None.
        """
        dump = payload.model_dump()
        processed_messages = []
        for message in dump:
            role = message.get("role")
            processed_messages.append(
                {
                    "role": role,
                    "content": self._preprocess_message(message.get(("message"))),
                }
            )
        return {"messages": processed_messages, "characters": self.registred_characters}

    def _postprocess_message(
        self, message: Optional[Union[str | tuple | list]]
    ) -> str | FileMessage | None:
        if not message:
            return None
        elif isinstance(message, (tuple, list)):
            filepath = str(message[0])

            mime_type = client_utils.get_mimetype(filepath)
            return FileMessage(
                file=FileData(path=filepath, mime_type=mime_type),
                alt_text=message[1] if len(message) > 1 else None,
            )
        elif isinstance(message, str):
            message = inspect.cleandoc(message)
            return message
        else:
            raise ValueError(f"Invalid message for MultiChat component: {message}")

    def postprocess(
        self,
        value: Optional[List[Dict[str, str | list | None]]],
    ) -> ChatbotData:
        """
        Parameters:
            value: Receives a list of dictionaries containing dictionaries with both \"role\" and \"content\" in each, the \"role\" can be registred in characters, there is a default \"user\" and \"bot\" profile in there if its needed.

        Returns:
            ChatbotData

        Example:
        ```python
            value = [{\"role\": \"Carl\", \"content\":\"Hi John, how are you doing?\"}, {\"role\": \"John\", \"content\":\"Hi Carl, I'm fine thank you for asking.\"}, {\"role\": \"Gustavo\", \"content\":\"Hi Carl and John!\"}]
        """
        if not value:
            return ChatbotData(root=[])
        self._load_characters(self.characters)
        processed_messages = []
        for message in value:
            if not isinstance(message, dict):
                raise TypeError(f"Expected a list of dictionaries. Received: {message}")
            char_name = message.get("role")
            char_content = message.get("content")
            if not isinstance(char_name, str) or not char_name.strip():
                raise ValueError(
                    f"Invalid role, it must be a non-empty string. Received: '{char_name}'"
                )

            char_data = self.registred_characters.get(char_name, {"position": "bot"})
            processed_messages.append(
                {
                    "role": char_name,
                    "message": self._postprocess_message(char_content),
                    "avatar": char_data.get("avatar"),
                    "position": char_data.get("position"),
                    "style": char_data.get("style"),
                }
            )
        return ChatbotData(root=processed_messages)

    def example_inputs(self) -> Any:
        return [
            {"role": "user", "content": "Hi!"},
            {"role": "bot", "content": "Hello there!"},
        ]
