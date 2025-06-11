return {
  "nvim-neo-tree/neo-tree.nvim",
  opts = {
    filesystem = {
      filtered_items = {
        visible = true, -- Hiện các mục bị ẩn
        show_hidden_count = true,
        hide_dotfiles = false, -- ❗ Hiện file .env, .gitignore, v.v.
        hide_gitignored = false, -- (nếu muốn hiện cả file bị git ignore)
      },
    },
  },
}
