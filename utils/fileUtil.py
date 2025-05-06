# import markdown2
# from weasyprint import HTML
# import tempfile


# def markdown_to_pdf(markdown_text):
#     # 将 Markdown 转 HTML
#     html_content = markdown2.markdown(markdown_text)
#
#     # 创建临时文件路径
#     with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpfile:
#         pdf_path = tmpfile.name
#
#     # 将 HTML 转 PDF 并保存到临时文件
#     HTML(string=html_content).write_pdf(pdf_path)
#
#     return pdf_path


import pdfkit

def markdown_to_pdf2(markdown_content):
    output_path = "output.pdf"
    pdfkit.from_string(markdown_content, output_path)
    return output_path
