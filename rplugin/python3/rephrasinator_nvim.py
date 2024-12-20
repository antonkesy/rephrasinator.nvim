import pynvim
from rephrasinator import get_rephrased_sentence, test


@pynvim.plugin
class Rephrasinator:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("TR", nargs="*", range="")
    def test_rephrasinator(self, args, range):
        if not range:
            return
        start_line, end_line = range
        selected_text = self.nvim.current.buffer[start_line - 1 : end_line]

        if len(selected_text) == 1 and selected_text[0] == "":
            return

        choices = test("".join(selected_text).strip())

        self.nvim.exec_lua(
            """
            local choices, start_line, end_line = ...
            require('rephrasinator').show_picker(choices, start_line, end_line)
            """,
            choices,
            start_line,
            end_line,
        )
