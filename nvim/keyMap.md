

# language supper
| where |     keys    |                          tác dụng                         |
|:-----:|:-----------:|:---------------------------------------------------------:|
| N     | gd          | Đi đến vị trí khai báo (định nghĩa)                       |
| N     | K           | Hiển thị thông tin chi tiết của biến hoặc hàm (hover)     |
| N     | <leader>vws | Tìm kiếm symbol trong toàn bộ workspace                   |
| N     | <leader>vd  | Mở cửa sổ nổi hiển thị thông tin lỗi/warning (diagnostic) |
| N     | [d          | Chuyển đến lỗi/warning tiếp theo                          |
| N     | ]d          | Chuyển đến lỗi/warning trước đó                           |
| N     | <leader>vca | Mở menu hành động mã (code actions)                       |
| N     | <leader>vrr | Tìm tất cả tham chiếu (references) của symbol             |
| N     | <leader>vrn | Đổi tên symbol (rename)                                   |
| I     | <C-h>       | Hiển thị trợ giúp chữ ký hàm (signature help)             |
| I     | <C-p>       | Pre supper                                                |
| I     | <C-n>       | Next supper                                               |



# bufferline
chuyển tab
| where | keys      | tác dụng                              |
|:-----:|:---------:|:--------------------------------------:|
| N     | L         | Chuyển đến buffer tiếp theo           |
| N     | H         | Chuyển đến buffer trước đó            |
| N     | <leader>bc| Đóng buffer hiện tại                  |
| N     | <leader>1 | Chuyển đến buffer thứ 1               |
| N     | <leader>2 | Chuyển đến buffer thứ 2               |


# find
| where | keys        | tác dụng                                   |
|:-----:|:-----------:|:------------------------------------------:|
| N     | <leader>ff  | Tìm kiếm file trong thư mục làm việc       |
| N     | <leader>fg  | Tìm kiếm chuỗi (grep) trong tất cả file    |
| N     | <leader>fb  | Tìm kiếm buffer đang mở                    |
| N     | <leader>fh  | Tìm kiếm lệnh/lịch sử tìm kiếm             |
| N     | <leader>fs  | Tìm kiếm symbol LSP trong project          |


# nvim-tree
| where | keys        | tác dụng                                   |
|:-----:|:-----------:|:------------------------------------------:|
| N     | <leader>e   | Mở/đóng sidebar Nvim-tree                  |
| N     | <leader>tf  | Tìm file hiện tại trong Nvim-tree          |


# commant
| where | keys        | tác dụng                                            |
|:-----:|:-----------:|:---------------------------------------------------:|
| N     | <leader>/   | Comment/uncomment dòng hiện tại                     |
| V     | <leader>/   | Comment/uncomment vùng được chọn                    |
| N     | gcc         | Comment/uncomment dòng hiện tại (không cần leader)  |
| V     | gc          | Comment/uncomment vùng được chọn (không cần leader) |


# vim surround
| where | keys          | tác dụng                                              |
|:-----:|:-------------:|:-----------------------------------------------------:|
| N     | <leader>sd    | Xóa cặp ký tự bao quanh (tương đương ds)              |
| N     | <leader>sc    | Thay đổi cặp ký tự bao quanh (tương đương cs)         |
| N     | <leader>sa    | Thêm cặp ký tự bao quanh cho motion (tương đương ys)  |
| N     | <leader>ss    | Bao quanh cả dòng hiện tại (tương đương yss)          |
| V     | <leader>s     | Bao quanh vùng text được chọn trong visual mode       |

