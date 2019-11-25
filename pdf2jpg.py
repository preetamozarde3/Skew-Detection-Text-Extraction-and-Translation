from pdf2image import convert_from_path

pages = convert_from_path('Hard_Copy_data_Scan_Delhi_Hindi.pdf', 500)
i = 0
for page in pages:
    img_name = 'img_'+str(i)+'.jpg'
    print(img_name)
    page.save(img_name, 'JPEG')
    i = i + 1
