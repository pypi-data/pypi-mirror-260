"""The main flexdown module."""
import importlib
import os
import shutil
import sys
from typing import Callable, Iterator

import reflex as rx

from flexdown import blocks, utils, types
from flexdown.blocks.block import Block
from flexdown.document import Document


DEFAULT_BLOCKS = [
    blocks.ExecBlock,
    blocks.EvalBlock,
    blocks.CodeBlock,
    blocks.MarkdownBlock,
]

files = {}


class Flexdown(rx.Base):
    """Class to parse and render flexdown files."""

    # The list of accepted block types to parse.
    block_types: list[type[Block]] = []

    # The default block type.
    default_block_type: type[Block] = blocks.MarkdownBlock

    # The template to use when rendering pages.
    page_template: Callable[[rx.Component], rx.Component] = rx.fragment

    # Mapping from markdown tag to a rendering function for Reflex components.
    component_map: types.ComponentMap = {}

    # The directory to save modules to.
    module_dir: str = "modules"

    def clear_modules(self):
        """Clear the modules directory."""
        # Get the path to the directory where the module should be saved.
        flexdown_dir = os.path.dirname(os.path.abspath(__file__))
        module_dir = os.path.join(flexdown_dir, self.module_dir)

        # Delete the directory.
        if os.path.exists(module_dir):
            shutil.rmtree(module_dir)

    def _get_block(self, line: str, line_number: int, filename=None) -> Block:
        """Get the block type for a line of text.

        Args:
            line: The line of text to check.
            line_number: The line number of the line.

        Returns:
            The block type for the line of text.
        """
        block_types = self.block_types + DEFAULT_BLOCKS

        # Search for a block type that can parse the line.
        for block_type in block_types:
            # Try to create a block from the line.
            block = block_type.from_line(
                line,
                line_number=line_number,
                component_map=self.component_map,
                filename=filename,
            )

            # If a block was created, then return it.
            if block is not None:
                return block

        # If no block was created, then return the default block type.
        return self.default_block_type().append(line)

    def exec(self, content: str, env: types.Env = {}, filename: str | None = None):
        # Get the path to the directory where the module should be saved.
        flexdown_dir = os.path.dirname(os.path.abspath(__file__))
        module_dir = os.path.join(flexdown_dir, self.module_dir)

        # Write the content to a file in the module directory.
        os.makedirs(module_dir, exist_ok=True)

        # Change this to append to the same file
        if filename in files:
            module_name = files[filename]
        else:
            # module_name = rx.vars.get_unique_variable_name()
            module_name = utils.get_id(filename)
            files[filename] = module_name
        module_path = os.path.join(module_dir, f"{module_name}.py")
        with open(module_path, "a", encoding="utf-8") as f:
            f.write(content + "\n")

        # Import the module to execute the code.
        module_name = f"flexdown.{self.module_dir}.{module_name}"
        os.environ["PYTEST_CURRENT_TEST"] = "1"
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)
        del os.environ["PYTEST_CURRENT_TEST"]

        env.update(vars(module))

    def get_blocks(self, source: str, filename: str | None = None) -> Iterator[Block]:
        """Parse a Flexdown file into blocks.

        Args:
            source: The source code of the Flexdown file.

        Returns:
            The iterator of blocks in the Flexdown file.
        """
        current_block = None

        # Iterate over each line in the source code.
        for line_number, line in enumerate(source.splitlines()):
            # If there is no current block, then create a new block.
            if current_block is None:
                # If the line is empty, then skip it.
                if line == "":
                    continue

                # Otherwise, create a new block.
                current_block = self._get_block(line, line_number, filename)

            else:
                # Add the line to the current block.
                current_block.append(line)

            # Check if the current block is finished.
            if current_block.is_finished():
                yield current_block
                current_block = None

        # Add the final block if it exists.
        if current_block is not None:
            current_block.finish()
            yield current_block

    def render(self, source: str | Document, filename=None) -> rx.Component:
        """Render a Flexdown file into a Reflex component.

        Args:
            source: The source code of the Flexdown file.

        Returns:
            The Reflex component representing the Flexdown file.
        """
        # Convert the source to a document.
        if isinstance(source, str):
            source = Document.from_source(source)

        # The environment used for execing and evaling code.
        env: types.Env = source.metadata
        env["__xd"] = self

        # Get the content of the document.
        source = source.content

        # Render each block.
        out: list[rx.Component] = []
        for block in self.get_blocks(source, filename):
            try:
                out.append(block.render(env=env))
            except Exception as e:
                print(
                    f"Error while rendering {type(block)} on line {block.start_line_number}. "
                    f"\n{block.get_content(env)}"
                )
                raise e

        # Wrap the output in the page template.
        return self.page_template(rx.fragment(*out))

    def render_file(self, path: str) -> rx.Component:
        """Render a Flexdown file into a Reflex component.

        Args:
            path: The path to the Flexdown file.

        Returns:
            The Reflex component representing the Flexdown file.
        """
        # Render the source code.
        return self.render(Document.from_file(path), path)

    def create_app(self, path: str) -> rx.App:
        """Create a Reflex app from a directory of Flexdown files.

        Args:
            path: The path to the directory of Flexdown files.

        Returns:
            The Reflex app representing the directory of Flexdown files.
        """
        project_path = os.path.abspath(path).rsplit("/", 1)[0]
        sys.path.append(project_path)

        try:
            # Get all the flexdown files in the directory.
            files = utils.get_flexdown_files(path)

            # Create the Reflex app.
            app = rx.App()

            # Add each page to the app.
            for file in files:
                route = file.replace(path, "").replace(".md", "")
                app.add_page(self.render_file(file), route=route)

            # Return the app.
            return app

        finally:
            sys.path.remove(project_path)
