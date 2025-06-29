require('nvim-tree').setup()
vim.keymap.set('n', '<leader>e', ':NvimTreeToggle<CR>', { desc = 'Mở/đóng Nvim-tree' })
vim.keymap.set('n', '<leader>tf', ':NvimTreeFindFile<CR>', { desc = 'Tìm file trong Nvim-tree' })
