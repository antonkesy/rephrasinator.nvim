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

local prompt_request = function(prompt)
  vim.cmd("RephrasinatorUpdatePrompt " .. prompt)
  return results
end

M.show_picker = function(original_text, choices, start_line, start_col, end_col)
  results = choices or {}

  picker = require("telescope.pickers").new({}, {
    prompt_title = "Rephrasinator",
    finder = require("telescope.finders").new_dynamic({
      fn = prompt_request,
      entry_maker = function(entry)
        return {
          value = entry,
          display = entry,
          ordinal = entry,
        }
      end,
    }),
    previewer = require("telescope.previewers").new_buffer_previewer({
      define_preview = function(self, entry)
        local clean_original_text = original_text:gsub("\n", " ")
        local clean_entry_value = entry.value:gsub("\n", " ")
        vim.api.nvim_buf_set_lines(self.state.bufnr, 0, -1, false,
          { "", clean_original_text, "->", clean_entry_value })
        vim.api.nvim_buf_add_highlight(self.state.bufnr, -1, "TelescopePreviewMatch", 1, 0, -1)
      end,
    }),
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

  -- Stop choice generation when the picker is closed
  local win_id = picker.prompt_win
  vim.api.nvim_create_autocmd("WinClosed", {
    pattern = tostring(win_id),
    callback = function()
      vim.cmd("RephrasinatorStop")
    end,
  })
end

M.add_to_picker = function(choice)
  if not picker then
    return
  end

  table.insert(results, choice)
  picker:refresh(require("telescope.finders").new_dynamic({ fn = prompt_request, }))

  local current_selection = require("telescope.actions.state").get_selected_entry()
  local new_selection = nil
  local state = require("telescope.actions.state")
  local prompt_bufnr = state.get_current_picker(picker.prompt_bufnr)

  if (not prompt_bufnr) or (not current_selection) then
    return
  end

  for i, entry in ipairs(results) do
    if entry == current_selection.value then
      new_selection = i
      break
    end
  end

  if new_selection then
    for i = 1, 50 do -- TODO: hack to get less flickering without async adding entries
      vim.defer_fn(function()
        prompt_bufnr:set_selection(new_selection - 1)
      end, i)
    end
  end
end

M.clear_results = function()
  results = {}
end

return M
