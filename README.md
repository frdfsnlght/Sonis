# Sonis
A music stand reader

## Testing

Parallel rendering:
setDocument: anger a.pdf
PDFDocument.vue:74 fetchPDF: 354.68603515625ms
PDFDocument.vue:58 getPages: 46.989990234375ms
PDFPage.vue:81 page 5: 6221.714111328125ms
PDFPage.vue:81 page 6: 6464.220947265625ms
PDFPage.vue:81 page 7: 6585.14501953125ms
PDFPage.vue:81 page 4: 11989.989013671875ms
PDFPage.vue:81 page 3: 12873.047119140625ms
PDFPage.vue:81 page 2: 13953.2958984375ms
PDFPage.vue:81 page 1: 26641.468994140625ms

Sequential rendering:

