-- This file can be loaded by calling `lua require('plugins')` from your init.vim

-- Only required if you have packer configured as `opt`
vim.cmd [[packadd packer.nvim]]

return require('packer').startup(function(use)
     -- Packer can manage itself
     use 'wbthomason/packer.nvim'

     -- Navigation
     use {
          'nvim-telescope/telescope.nvim', tag = '0.1.8',
          -- or                            , branch = '0.1.x',
          requires = { {'nvim-lua/plenary.nvim'} }
     }
     use 'folke/zen-mode.nvim'
     use( 'ThePrimeagen/harpoon')
     use { 'kyazdani42/nvim-tree.lua', requires = { 'kyazdani42/nvim-web-devicons' } }

     -- theme
     use({
          'rose-pine/neovim',
          as = 'rose-pine',
          config = function()
               vim.cmd('colorscheme rose-pine')
          end
     })
     use { "catppuccin/nvim", as = "catppuccin" }
     use 'folke/tokyonight.nvim'
     use 'kyazdani42/nvim-web-devicons'

     -- lang hightline
     use( 'nvim-treesitter/nvim-treesitter', { run = ':TSUpdate'})
     use 'nvim-treesitter/nvim-treesitter-textobjects'
     use( 'nvim-treesitter/playground')

     -- Editting enchancements
     use( 'mbbill/undotree')
     use( 'tpope/vim-fugitive')
     use 'tpope/vim-surround'
     use { 'windwp/nvim-autopairs', config = function() require('nvim-autopairs').setup() end }

     -- UI
     use { 'nvim-lualine/lualine.nvim', requires = { 'kyazdani42/nvim-web-devicons' } }
     use { 'akinsho/bufferline.nvim', requires = { 'kyazdani42/nvim-web-devicons' } }
     use { 'akinsho/toggleterm.nvim', tag = '*', config = function() require('toggleterm').setup() end }

     -- lang support
     use 'numToStr/Comment.nvim'
     use {
          'VonHeikemen/lsp-zero.nvim',
          branch = 'v3.x',
          requires = {
               -- LSP Support
               {'neovim/nvim-lspconfig'},
               {'williamboman/mason.nvim'},
               {'williamboman/mason-lspconfig.nvim'},

               -- Autocomplention
               {'hrsh7th/nvim-cmp'},
               {'hrsh7th/cmp-buffer'},
               {'hrsh7th/cmp-path'},
               {'saadparwaiz1/cmp_luasnip'},
               {'hrsh7th/cmp-nvim-lsp'},
               {'hrsh7th/cmp-nvim-lua'},

               -- Snippets
               {'L3MON4D3/LuaSnip'},
               {'rafamadriz/friendly-snippets'},
          }
     }
     use {
          'rmagatti/auto-session',
          config = function()
               require("auto-session").setup {
                    suppressed_dirs = { "~/", "~/Projects", "~/Downloads", "/"},
               }
          end
     }

end)
