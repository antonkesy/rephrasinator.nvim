local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    lazypath
  })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  {
    "antonkesy/rephrasinator.nvim",
    dependencies = {
      "nvim-telescope/telescope.nvim",
    },
    build = ":UpdateRemotePlugins",
    init = function()
      require("rephrasinator").setup()
    end,
  },
})

vim.g.mapleader = " "
