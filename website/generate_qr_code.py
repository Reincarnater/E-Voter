import pyotp
import qrcode
import os
key = "ResearchGroupProgrammerSecretKey"

uri = pyotp.totp.TOTP(key).provisioning_uri(name="E-Voter",
                                                issuer_name="E-Voter Website")
print(uri)
# Ensure the static/images directory exists
output_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the QR code image into the static/images directory
qrcode.make(uri).save(os.path.join(output_dir, "QR_Code.png"))