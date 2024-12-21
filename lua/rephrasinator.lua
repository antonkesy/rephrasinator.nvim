local M = {}

M.setup = function()
  if not vim.fn.exists(":Rephrasinator") then
    vim.notify("Rephrasinator setup failed: 'Rephrasinator' command not found", vim.log.levels.ERROR)
    return
  end

  require("telescope").setup({
    defaults = {
      layout_config = {
        width = 0.8,
        height = 0.4,
      },
      file_ignore_patterns = { "node_modules" },
    },
  })

  vim.api.nvim_set_keymap(
    "v",
    "<leader>rp",
    "<cmd>Rephrasinator<CR>",
    { noremap = true, silent = true }
  )
end

local results = {}
local picker = nil

M.is_picker_open = function()
  return picker ~= nil
end

M.show_picker = function(choices, start_line, start_col, end_col)
  results = choices or {}

  picker = require("telescope.pickers").new({}, {
    finder = require("telescope.finders").new_table({
      results = results,
      entry_maker = function(entry)
        return {
          value = entry,
          display = entry,
          ordinal = entry,
        }
      end,
    }),
    sorter = require("telescope.config").values.generic_sorter({}),
    attach_mappings = function(_, map)
      map('i', '<CR>', function(prompt_bufnr)
        local selection = require("telescope.actions.state").get_selected_entry()
        require("telescope.actions").close(prompt_bufnr)
        if selection then
          -- Replace only the selected part of the text, not the entire line
          local line = vim.api.nvim_buf_get_lines(0, start_line, start_line + 1, false)[1]
          local new_line = line:sub(1, start_col) .. selection.value .. line:sub(end_col + 1)
          vim.api.nvim_buf_set_lines(0, start_line, start_line + 1, false, { new_line })
        end
      end)
      return true
    end,
  })

  picker:find()
end

M.add_to_picker = function(choice)
  if not picker then
    return
  end

  table.insert(results, choice)

  picker:refresh(require("telescope.finders").new_table({
    results = results,
    entry_maker = function(entry)
      return {
        value = entry,
        display = entry,
        ordinal = entry,
      }
    end,
  }), require("telescope.config").values.generic_sorter({}))
end

return M
