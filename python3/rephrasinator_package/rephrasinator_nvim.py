import pynvim as vim
from rephrasinator import get_rephrased_sentence


class Rephrasinator:

    def test(self) -> None:
        answers = get_rephrased_sentence("I am a test", None)
        print(answers)
        vim.command(":echo 'filetype not supported but as vim message'")
