import pynvim
from rephrasinator import get_rephrased_sentence, test


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

        # choices = get_rephrased_sentence(selected_text.strip())
        choices = test(selected_text.strip())

        self.nvim.exec_lua(
            """
            local choices, start_line, end_line, selected_text = ...
            require('rephrasinator').show_picker(choices, start_line, end_line, selected_text)
            """,
            choices,
            range[0],
            range[1],
            selected_text,
        )
