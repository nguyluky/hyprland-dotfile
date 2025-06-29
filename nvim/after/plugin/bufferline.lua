-- ~/.config/nvim/lua/bufferline-config.lua
require('bufferline').setup {
    options = {
        mode = 'buffers', -- Hiển thị buffer thay vì tab
        numbers = 'ordinal', -- Hiển thị số thứ tự (1, 2, 3,...) như tab
        close_command = 'bdelete! %d', -- Lệnh đóng buffer
        right_mouse_command = 'bdelete! %d', -- Chuột phải để đóng
        diagnostics = 'nvim_lsp', -- Hiển thị lỗi LSP từ lsp-zero
        diagnostics_indicator = function(count) return '(' .. count .. ')' end,
        offsets = { { filetype = 'NvimTree', text = 'File Explorer', padding = 1 } }, -- Dành chỗ cho Nvim-tree
        show_buffer_icons = true, -- Bật icon file
        show_close_icon = true, -- Hiển thị nút đóng
        separator_style = 'slant', -- Kiểu phân cách tab
    },
}

-- Keybindings
vim.keymap.set('n', 'K', ':BufferLineCycleNext<CR>', { desc = 'Bufferline: Buffer tiếp theo' })
vim.keymap.set('n', 'J', ':BufferLineCyclePrev<CR>', { desc = 'Bufferline: Buffer trước đó' })
vim.keymap.set('n', '<leader>bc', ':bdelete<CR>', { desc = 'Bufferline: Đóng buffer' })
vim.keymap.set('n', '<leader>1', ':BufferLineGoToBuffer 1<CR>', { desc = 'Bufferline: Chuyển đến buffer 1' })
vim.keymap.set('n', '<leader>2', ':BufferLineGoToBuffer 2<CR>', { desc = 'Bufferline: Chuyển đến buffer 2' })
