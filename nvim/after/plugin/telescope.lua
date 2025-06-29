
local telescope = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', telescope.find_files, { desc = 'Tìm file' })
vim.keymap.set('n', '<leader>fg', telescope.live_grep, { desc = 'Grep chuỗi' })
vim.keymap.set('n', '<leader>fb', telescope.buffers, { desc = 'Tìm buffer' })
vim.keymap.set('n', '<leader>fh', telescope.help_tags, { desc = 'Tìm help' })
vim.keymap.set('n', '<leader>fs', telescope.lsp_document_symbols, { desc = 'Tìm symbol' })
