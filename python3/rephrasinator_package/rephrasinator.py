import pynvim as vim


class Rephrasinator:

    def test(self) -> None:
        print("filetype not supported")
        vim.command(":echo 'filetype not supported but as vim message'")
