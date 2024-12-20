local M = {}

M.show_picker = function(choices, start_line, end_line, highlight_text)
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

        -- Set the preview buffer lines
        vim.api.nvim_buf_set_lines(bufnr, 0, -1, false, new_lines)

        -- Apply syntax highlighting
        local filetype = vim.bo.filetype
        vim.api.nvim_buf_set_option(bufnr, 'filetype', filetype)

        -- Find the start and end positions of the highlight_text
        local line_to_highlight = entry.value
        local start_col, end_col = nil, nil
        if highlight_text then
          start_col = line_to_highlight:find(highlight_text, 1, true) -- Plain text search
          if start_col then
            end_col = start_col + #highlight_text - 1
          end
        end

        -- Highlight the specific portion of the line
        if start_col and end_col then
          vim.api.nvim_buf_add_highlight(bufnr, -1, 'TelescopePreviewLine', start_line - 1, start_col - 1, end_col)
        end

        -- Center the highlight in the preview
        vim.api.nvim_buf_call(bufnr, function()
          vim.fn.cursor(start_line, 0)
          vim.cmd("normal! zz") -- Center the highlighted line
        end)
      end,
    }),
    attach_mappings = function(_, map)
      map('i', '<CR>', function(prompt_bufnr)
        local selection = require("telescope.actions.state").get_selected_entry()
        require("telescope.actions").close(prompt_bufnr)
        vim.api.nvim_buf_set_lines(0, start_line - 1, end_line, false, { selection.value })
      end)
      return true
    end,
  }):find()
end

return M
