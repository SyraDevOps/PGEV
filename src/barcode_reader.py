import qrcode

class BarcodeReader:
    def __init__(self):
        pass

    def generate_barcode(self, product_id):
        import barcode
        from barcode.writer import ImageWriter
        
        code128 = barcode.get('code128', product_id, writer=ImageWriter())
        filename = code128.save(f'barcodes/{product_id}')
        return filename

    def read_barcode(self, image_path):
        from PIL import Image
        from pyzbar.pyzbar import decode
        
        image = Image.open(image_path)
        decoded_objects = decode(image)
        return [obj.data.decode('utf-8') for obj in decoded_objects]

    def generate_qrcode(self, data, filename):
        img = qrcode.make(data)
        img.save(f'qrcode/{filename}.png')
        return f'qrcode/{filename}.png'