from __future__ import annotations
from .import AutoGPTPDFToText
import fitz
import os
import tiktoken

plugin = AutoGPTPDFToText()
one_chunk = 4000 #amount of token in one chunk


def split_text_into_chunks(text: str, encoding_name: str, chunk_size: int) -> list:
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)
    chunks = []
    current_chunk = []
    current_size = 0

    for token in tokens:
        current_chunk.append(token)
        current_size += 1  # Increment size by 1 for each token
        if current_size >= chunk_size:
            chunks.append(current_chunk)
            current_chunk = []
            current_size = 0
    
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

def pdf2txt(pdf_file_name: str, txt_file_name: str) -> str:
    """Convert a PDF file to a text file.
    Args:
        pdf_filen_name (str): The PDF file path.
        txt_filen_name (str): The TXT file path.
    Returns:
        str: The tweet that was posted.
    """

    dirname = os.path.dirname(__file__)
    cwd = os.path.join(dirname, '../../../../../../autogpt/auto_gpt_workspace')
    cwd = os.path.normpath(cwd)

    doc = fitz.open(cwd + '/' + pdf_file_name) # open a document
    content = "" # Initialize the content variable
    for page in doc: # iterate the document pages
        text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
        content += text.decode("utf8")

    chunks_text = split_text_into_chunks(content, "cl100k_base", one_chunk)

    # Save each chunk to a separate file
    # divide filename and extention
    file_name_without_extension, _ = os.path.splitext(txt_file_name)
    # if no directory, then make a directory
    if not os.path.exists(cwd + '/'+file_name_without_extension):
        os.makedirs(cwd + '/'+file_name_without_extension)
    for i, chunk in enumerate(chunks_text):
        # Construct the filename for each chunk
        filename = os.path.join(cwd + '/'+file_name_without_extension, f'{file_name_without_extension}_chunk_{i}.txt') #directory and file name to save the text data
        with open(filename, 'w', encoding='utf-8') as file:
            encoding = tiktoken.get_encoding("cl100k_base")
            decoded_text = encoding.decode(chunk)
            file.write(decoded_text)


    return "Success! The PDF file was converted to a text file."