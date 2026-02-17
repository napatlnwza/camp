import qrcode

data = "https://napatlnwza.github.io/webpassword/"
img = qrcode.make(data)
img.save("qrcode.png")
print("สร้าง QR Code สำเร็จ")