PyPdfOps: Python PDF Operations Library
=======================================

PyPdfOps is a Python library that simplifies the manipulation of PDF files. It provides a set of methods for common PDF operations, including compression, conversion to different formats (pptx, images, doc), splitting, and merging. With PyPdfOps, you can streamline your PDF-related tasks in your Python projects.

### Check out the library on PYPI
[PyPDFOps PYPI Repository](https://pypi.org/project/pypdfops/)

Installation
------------

    pip install pypdfops
    

Usage
-----

### 1\. PDF Compression

For compressing pdf, PDFNet sdk is used and a token is required to use the compressing feature. To obtain a demo token, head to 'https://dev.apryse.com/get-key', after signin, choose web and get the trial key.

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf"
output_pdf = "compressed_output.pdf"
pdf = PDFOps(token = "COMPRESSION_TOKEN") # Token for compression
pdf.compress_pdf(input_pdf, output_pdf)
```
    

### 2\. PDF to PPTX Conversion

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf"
output_pptx = "converted_pdf.pptx"
pdf = PDFOps()
pdf.convert_to_pptx(input_pdf, output_pptx)
```
        
    

### 3\. PDF to Images Conversion

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf"
output_folder = "Images"
pdf = PDFOps()
pdf.extract_pages_as_images(input_pdf, output_folder)
```
        
    

### 4\. PDF to DOC Conversion

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf"
output_doc = "converted_pdf.doc"
pdf = PDFOps()
pdf.convert_to_doc(input_pdf, output_doc)
```
        
    

### 5\. PDF Splitting

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf"
output_folder = "SplittedPdfs"
pages_to_split = [[1,2],[3,5]]
pdf = PDFOps()
pdf.split_pdf(input_pdf, output_folder,pages_to_split)
```
        
    

### 6\. PDF Merging

```python
from pypdfops import PDFOps 
input_pdfs = [
    "input1.pdf",
    "input2.pdf",
    "input3.pdf"
]
output_pdf = "Merged.pdf"
pdf = PDFOps()
pdf.merge_pdfs(input_pdfs, output_pdf)
```



### 7\. PDF Encryption

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf
output_pdf = "encrypted.pdf"
password = "12345678"
pdf = PDFOps()
pdf.encrypt_pdf(input_pdf, output_pdf, password)
```


### 8\. PDF Decryption

```python
from pypdfops import PDFOps 
input_pdf = "input.pdf
output_pdf = "decrypted.pdf"
password = "12345678"
pdf = PDFOps()
pdf.decrypt_pdf(input_pdf, output_pdf, password)
```
    

Feel free to customize the examples and add more details to suit your specific use cases.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)