# 실제투자로 진행할 시 True를 False로 변경
is_paper_trading = True

# 따옴표 안에 작성할 것
real_app_key = "97K_iySp17_oD2_0DM-ENbOwp4T-6VOW6mOVBvs6oaE"
real_app_secret = "gnjmXXi6obPw0VCiPaWcVVizUr6N3CZlxIBJSxxIisE"

paper_app_key = "_7giDnyjX4Cqi9oYOBxLo5xQdai8x1T16C-2O_gSX-I"
paper_app_secret = "ibfWcn7Bx4DfXZXG6RKKIyus89XglzdO8oZ4l8VQ9Jg"

real_host_url = "https://api.kiwoom.com"
paper_host_url = "https://mockapi.kiwoom.com"

real_socket_url = "wss://api.kiwoom.com:10000"
paper_socket_url = "wss://mockapi.kiwoom.com:10000"

app_key = paper_app_key if is_paper_trading else real_app_key
app_secret = paper_app_secret if is_paper_trading else real_app_secret
host_url = paper_host_url if is_paper_trading else real_host_url
socket_url = paper_socket_url if is_paper_trading else real_socket_url

telegram_chat_id = "6851048747"
telegram_token = "8226990977:AAGTTuAmxVX_wN5W4cuo_h9hVtKoGNJHIqE"