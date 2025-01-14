import qrcode
import pyotp


key = "E-VoterWebsiteSuperSecretKey"


uri = pyotp.totp.TOTP(key).provisioning_uri(name="E-Voter Votee",
                                            issuer_name="E-Voter Web App")

QR_CODE = qrcode.make(uri).save("QR_Code.png")
