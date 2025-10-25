
import pypandoc

def word_to_pdf(docx_path, output_path):
    """Convert DOCX to PDF using pypandoc"""
    pypandoc.convert_file(docx_path, 'pdf', outputfile=output_path)
    return output_path

# def document_to_pdf(input_path, output_path, input_format=None):
#     """Convert various document formats to PDF"""
#     if input_format == 'html':
#         HTML(filename=input_path).write_pdf(output_path)
#     elif input_format == 'md':
#         html = markdown.markdown(open(input_path).read())
#         HTML(string=html).write_pdf(output_path)
#     else:
#         pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
#     return output_path
