

-- ~/.config/nvim/lua/surround-config.lua
-- Ánh xạ lại các lệnh vim-surround với <leader>
local opts = { noremap = true, silent = true }

vim.keymap.set('n', '<leader>sd', ':<C-u>normal ds<CR>', { desc = 'Surround: Xóa surrounding', noremap = true })
vim.keymap.set('n', '<leader>sc', ':<C-u>normal cs<CR>', { desc = 'Surround: Thay đổi surrounding', noremap = true })
vim.keymap.set('n', '<leader>sa', ':<C-u>normal ys<CR>', { desc = 'Surround: Thêm surrounding', noremap = true })
vim.keymap.set('n', '<leader>ss', ':<C-u>normal yss<CR>', { desc = 'Surround: Bao quanh cả dòng', noremap = true })
vim.keymap.set('v', '<leader>s', 'S', { desc = 'Surround: Bao quanh trong visual mode', noremap = true })

