local M = {}

M.show_picker = function(choices, start_line, end_line)
  require("telescope.pickers").new({}, {
    finder = require("telescope.finders").new_table({ results = choices }),
    sorter = require("telescope.config").values.generic_sorter({}),
    previewer = require("telescope.previewers").new_buffer_previewer({
      define_preview = function(self, entry, status)
        local bufnr = self.state.bufnr
        local lines = vim.fn.getbufline(0, 1, '$')
        local new_lines = vim.list_slice(lines, 1, start_line - 1)
        table.insert(new_lines, entry.value)
        for i = end_line + 1, #lines do
          table.insert(new_lines, lines[i])
        end
        vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, new_lines)
        vim.api.nvim_buf_add_highlight(bufnr, -1, 'TelescopePreviewLine', start_line - 1, 0, -1)
      end
    }),
    attach_mappings = function(_, map)
      map('i', '<CR>', function(prompt_bufnr)
        local selection = require("telescope.actions.state").get_selected_entry()
        require("telescope.actions").close(prompt_bufnr)
        vim.api.nvim_buf_set_lines(0, start_line - 1, end_line, false, { selection.value })
      end)
      return true
    end
  }):find()
end

return M
