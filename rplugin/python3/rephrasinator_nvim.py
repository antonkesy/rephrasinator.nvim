from typing import Set
import pynvim
import asyncio
from rephrasinator import get_rephrased_sentence


@pynvim.plugin
class Rephrasinator:
    NUMBER_OF_SUGGESTIONS = 30
    choices: Set[str]

    def __init__(self, nvim):
        self.nvim = nvim

    def get_visual_selection(self) -> str:
        buf = self.nvim.current.buffer
        start_pos = self.nvim.call("getpos", "v")
        end_pos = self.nvim.call("getpos", ".")
        start_line, start_col = start_pos[1] - 1, start_pos[2] - 1
        end_line, end_col = end_pos[1] - 1, end_pos[2]

        if start_line == end_line:  # Single line selection
            return buf[start_line][start_col:end_col]
        else:  # Multi-line selection
            selected_text = [buf[start_line][start_col:]]
            selected_text.extend(buf[start_line + 1 : end_line])
            selected_text.append(buf[end_line][:end_col])
            return "\n".join(selected_text)

    @pynvim.command("Rephrasinator", nargs="*", range="")
    def test_rephrasinator(self, _, range: range) -> None:
        selected_text = self.get_visual_selection()

        self.choices = set()

        if not selected_text.strip():
            return

        self.nvim.exec_lua(
            """
            local choices, start_line, end_line = ...
            require('rephrasinator').show_picker(choices, start_line, end_line)
            """,
            [],
            range[0],
            range[1],
        )

        asyncio.create_task(self.fill_choices(selected_text))

    async def get_choices(self, text_to_rephrase: str):
        for _ in range(self.NUMBER_OF_SUGGESTIONS):
            result = get_rephrased_sentence(text_to_rephrase)
            if result:
                yield result
            await asyncio.sleep(0.01)

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
