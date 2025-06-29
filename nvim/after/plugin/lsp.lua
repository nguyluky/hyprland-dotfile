
-- Tải lsp-zero
local lsp = require('lsp-zero')
require('luasnip.loaders.from_vscode').lazy_load() -- Loads React/TS snippets

-- Gắn các keymap mặc định và cấu hình LSP
lsp.preset('recommended')

-- (Tùy chọn) Cấu hình mason để cài đặt language server
require('mason').setup()
require('mason-lspconfig').setup({
    ensure_installed = { 
         -- 'tsserver',
         'eslint',
         'lua_ls', 
         'rust_analyzer',
    }, -- Thay bằng language server bạn cần
    handlers = {
        lsp.default_setup,
    },
})

-- Cấu hình nvim-cmp (autocompletion)
local cmp = require('cmp')
local cmp_action = lsp.cmp_action()

cmp.setup({
    sources = {
          {name = 'luasnip' },
        { name = 'nvim_lsp' },
        { name = 'buffer' },
        { name = 'path' },
    },
    mapping = cmp.mapping.preset.insert({
        ['<C-Space>'] = cmp.mapping.complete(),
        ['<C-e>'] = cmp.mapping.close(),
        ['<CR>'] = cmp.mapping.confirm({ select = true }),
        ['<C-p>'] = cmp_action.luasnip_supertab(),
        ['<C-n>'] = cmp_action.luasnip_shift_supertab(),
    }),
    snippet = {
        expand = function(args)
            require('luasnip').lsp_expand(args.body)
        end,
    },
})

-- Gắn các keymap mặc định của lsp-zero
lsp.on_attach(function(client, bufnr)
    local opts = { buffer = bufnr , remap = false}
    vim.keymap.set("n", "gd", function() vim.lsp.buf.definition() end, opts)
    vim.keymap.set("n", "<C-k>", function() vim.lsp.buf.hover() end, opts)
    vim.keymap.set("n", "<leader>vws", function() vim.lsp.buf.workspace_symbol() end, opts)
    vim.keymap.set("n", "<leader>vd", function() vim.diagnostic.open_float() end, opts)
    vim.keymap.set("n", "[d", function() vim.diagnostic.goto_next() end, opts)
    vim.keymap.set("n", "]d", function() vim.diagnostic.goto_prev() end, opts)
    vim.keymap.set("n", "<leader>vca", function() vim.lsp.buf.code_action() end, opts)
    vim.keymap.set("n", "<leader>vrr", function() vim.lsp.buf.references() end, opts)
    vim.keymap.set("n", "<leader>vrn", function() vim.lsp.buf.rename() end, opts)
    vim.keymap.set("i", "<C-h>", function() vim.lsp.buf.signature_help() end, opts)
end)

-- Áp dụng cấu hình
lsp.setup()
