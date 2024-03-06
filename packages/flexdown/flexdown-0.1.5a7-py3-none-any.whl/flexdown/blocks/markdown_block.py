from typing import Callable

import reflex as rx

from flexdown import types, utils
from flexdown.blocks.block import Block


class MarkdownBlock(Block):
    """A block of Markdown."""

    line_transforms = [
        utils.evaluate_templates,
    ]
    render_fn: Callable = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        @rx.memo
        def flexdown_memo(content: str) -> rx.Component:
            return rx.markdown(content, component_map=self.component_map)

        self.render_fn = flexdown_memo

    def render(self, env: types.Env) -> rx.Component:
        return self.render_fn(content=self.get_content(env))
