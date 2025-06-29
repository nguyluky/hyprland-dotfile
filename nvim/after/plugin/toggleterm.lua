
require('toggleterm').setup({
    size = 10, -- Height of horizontal terminal (or width if vertical)
    open_mapping = [[<C-\>]], -- Key to toggle terminal
    hide_numbers = true, -- Hide line numbers in terminal
    shade_terminals = true, -- Slightly darken terminal background
    start_in_insert = true, -- Start in insert mode
    insert_mappings = true, -- Allow <C-\> in insert mode
    terminal_mappings = true, -- Allow <C-\> in terminal mode
    persist_size = true, -- Remember terminal size
    direction = 'horizontal', -- Floating terminal (can change to 'horizontal', 'vertical', or 'tab')
    close_on_exit = true, -- Close terminal when process exits
    shell = vim.o.shell, -- Use default shell (e.g., bash, zsh)
    float_opts = {
        border = 'curved', -- Border style: 'single', 'double', 'curved'
        winblend = 0, -- Transparency (0 = opaque)
    },
})

