import asyncio
from dataclasses import dataclass
from typing import Optional, Set

import pynvim
from rephrasinator import get_rephrased_sentence


@pynvim.plugin
class Rephrasinator:
    NUMBER_OF_SUGGESTIONS = 100
    choices: Set[str]

    def __init__(self, nvim):
        self.nvim = nvim
        self.stop_event = asyncio.Event()
        self.prompt_request: Optional[str] = None

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
    def test_rephrasinator(self, *_) -> None:
        selection = self.get_visual_selection()
        if not selection:
            return

        self.choices = set()

        if not selection.text.strip():
            return

        self.nvim.exec_lua(
            """
            local original_text, choices, start_line, start_col, end_col = ...
            require('rephrasinator').show_picker(original_text, choices, start_line, start_col, end_col)
            """,
            selection.text,
            [],
            selection.start_line,
            selection.start_col,
            selection.end_col,
        )
        self.stop_event.clear()
        asyncio.create_task(self.fill_choices(selection.text))

    async def get_choices(self, text_to_rephrase: str):
        for _ in range(self.NUMBER_OF_SUGGESTIONS):
            result = get_rephrased_sentence(text_to_rephrase, self.prompt_request)
            if result:
                yield result
            await asyncio.sleep(0.001)

    async def fill_choices(self, selected_text: str) -> None:
        try:
            async for choice in self.get_choices(selected_text.strip()):
                if self.stop_event.is_set():
                    break

                # ensure unique choices
                if choice in self.choices:
                    continue
                self.choices.add(choice)

                self.nvim.async_call(
                    lambda: self.nvim.exec_lua(
                        """
                        local choice = ...
                        require('rephrasinator').add_to_picker(choice)
                        """,
                        choice,
                    )
                )
        except Exception as e:
            self.nvim.err_write(f"Error fetching choices: {e}\n")

    @pynvim.command("RephrasinatorStop", nargs="*")
    def stop_rephrasinator(self, *_):
        self.stop_event.set()

    @pynvim.command("RephrasinatorUpdatePrompt", nargs="*")
    def update_rephrasinator(self, args):
        prompt = " ".join(args)
        if prompt == self.prompt_request:
            return  # no need to update
        self.prompt_request = prompt
        self.choices = set()
        self.nvim.exec_lua(
            """
            require('rephrasinator').clear_results()
            """,
        )
