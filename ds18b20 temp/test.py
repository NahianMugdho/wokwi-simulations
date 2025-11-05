import serial

port = "ttyUSB0"  # তোমার VS Code এ যেটা দেখাচ্ছে
baud = 115200

ser = serial.Serial(port, baud)
print("[Connected to Wokwi Serial Port]\n")

while True:
    line = ser.readline().decode().strip()
    if line:
        print(f"[Wokwi Output] {line}")
