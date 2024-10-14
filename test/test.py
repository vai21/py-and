# Define the bytearray
byte_data = bytearray(b'\x16\x81\x00V\x00`\x00\xe8\x07\n\t\x0c%\x14L\x00\x00\x00')
byte_data2 = bytearray(b'\x16\x16\x01\x30\x30\x02\x52\x53\x03\x00')
# Convert bytearray to string
string_data = byte_data.decode('utf-8', errors='replace')
string_data2 = byte_data2.decode('utf-8', errors='replace')

print(string_data)
print(string_data2)