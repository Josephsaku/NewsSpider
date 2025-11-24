from fpdf import FPDF

# 导入配置
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import Config
except ImportError:
    # 如果配置文件不存在，使用默认配置
    class Config:
        PDF_FONT_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"

def to_pdf(pdf, title, author, publish_time, content):
    pdf.add_page()

    # 设置 macOS 中文字体
    pdf.add_font("Songti", "", Config.PDF_FONT_PATH)
    pdf.add_font("Songti", "B", Config.PDF_FONT_PATH)
    pdf.set_font("Songti", "", 12)

    # 标题（16pt，加粗）
    pdf.set_font(size=16, style="B")
    pdf.multi_cell(0, 10, title, align="C")
    pdf.ln(10)  # 换行

    # 作者和发布时间（12pt）
    pdf.set_font(size=12, style="")
    pdf.cell(0, 10, f"作者: {author}", ln=1)
    pdf.cell(0, 10, f"发布时间: {publish_time}", ln=1)
    pdf.ln(10)

    # 正文内容（10pt）
    pdf.set_font(size=10, style="")
    pdf.multi_cell(0, 8, content)  # 自动换行

    print("生成中...")