import pynvim
import asyncio
from rephrasinator import get_rephrased_sentence


async def test(t: str):
    examples = [
        t,
        t[::-1],
        "Rephrased sentence 1",
        "Rephrased sentence 2",
        "Rephrased sentence 3",
    ]
    for example in examples:
        await asyncio.sleep(0.5)
        yield example


@pynvim.plugin
class Rephrasinator:
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

        if not selected_text.strip():
            return

        # = get_rephrased_sentence(selected_text.strip())
        self.nvim.exec_lua(
            """
            local choices, start_line, end_line = ...
            require('rephrasinator').show_picker(choices, start_line, end_line)
            """,
            [],
            range[0],
            range[1],
        )

        asyncio.create_task(self.async_get_choices(selected_text))

    async def async_get_choices(self, selected_text: str) -> None:
        try:
            async for choice in test(selected_text.strip()):
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
