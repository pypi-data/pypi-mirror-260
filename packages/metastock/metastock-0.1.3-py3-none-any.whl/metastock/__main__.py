"""

Mục đích của file này là hỗ trợ gọi ở command line dạng `python -m metastock`

"""
from metastock.cli.pystock import app

app(prog_name="metastock")
app()
