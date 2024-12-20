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

        self.nvim.call(
            "luaeval",
            """
            require("telescope.pickers").new({}, {
                finder = require("telescope.finders").new_table({ results = _A }),
                sorter = require("telescope.config").values.generic_sorter({}),
                attach_mappings = function(_, map)
                    map('i', '<CR>', function(prompt_bufnr)
                        local selection = require("telescope.actions.state").get_selected_entry()
                        require("telescope.actions").close(prompt_bufnr)
                        vim.api.nvim_buf_set_lines(0, 0, -1, false, {selection[1]})
                    end)
                    return true
                end
            }):find()
            """,
            choices,
        )
