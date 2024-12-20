import pynvim
from rephrasinator import get_rephrased_sentence, test


@pynvim.plugin
class Rephrasinator:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command("TR", nargs="*", range="")
    def test_rephrasinator(self, args, range):
        answers = test()

        for i, a in enumerate(answers):
            answers[i] = str(i + 1) + " " + a

        choices = ["Select an answer:"] + answers

        choice = self.nvim.eval(f"inputlist({choices})")

        if choice > 0:
            selected_answer = answers[choice - 1]
            self.nvim.command(f"echo 'You selected: {selected_answer}'")
        else:
            self.nvim.command("echo 'No selection made'")
