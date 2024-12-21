import asyncio
from dataclasses import dataclass
from typing import Optional, Set

import pynvim
from rephrasinator import get_rephrased_sentence


@pynvim.plugin
class Rephrasinator:
    NUMBER_OF_SUGGESTIONS = 10
    choices: Set[str]

    def __init__(self, nvim):
        self.nvim = nvim

    @dataclass
    class Selection:
        text: str
        start_line: int
        start_col: int
        end_col: int

    def get_visual_selection(self) -> Optional[Selection]:
        buf = self.nvim.current.buffer
        start_pos = self.nvim.call("getpos", "v")
        end_pos = self.nvim.call("getpos", ".")
        start_line, start_col = start_pos[1] - 1, start_pos[2] - 1
        end_line, end_col = end_pos[1] - 1, end_pos[2]

        if start_line != end_line:
            self.nvim.err_write("Multi-line selection not supported\n")
            return None

        return Rephrasinator.Selection(
            buf[start_line][start_col:end_col], start_line, start_col, end_col
        )

    @pynvim.command("Rephrasinator", nargs="*", range="")
    def test_rephrasinator(self, _, _range: range) -> None:
        selection = self.get_visual_selection()
        if not selection:
            return

        self.choices = set()

        if not selection.text.strip():
            return

        self.nvim.exec_lua(
            """
            local choices, start_line, start_col, end_col = ...
            require('rephrasinator').show_picker(choices, start_line, start_col, end_col)
            """,
            [],
            selection.start_line,
            selection.start_col,
            selection.end_col,
        )
        asyncio.create_task(self.fill_choices(selection.text))

    async def get_choices(self, text_to_rephrase: str):
        for _ in range(self.NUMBER_OF_SUGGESTIONS):
            result = get_rephrased_sentence(text_to_rephrase)
            if result:
                yield result
            await asyncio.sleep(0.001)

    async def fill_choices(self, selected_text: str) -> None:
        try:
            async for choice in self.get_choices(selected_text.strip()):
                # ensure unique choices
                if choice in self.choices:
                    continue
                self.choices.add(choice)

                self.nvim.async_call(
                    lambda: self.nvim.exec_lua(
                        """
                        local choice = ...
                        print("Received choice in Lua:", choice)  -- Debugging log
                        require('rephrasinator').add_to_picker(choice)
                        """,
                        choice,
                    )
                )
        except Exception as e:
            self.nvim.err_write(f"Error fetching choices: {e}\n")
