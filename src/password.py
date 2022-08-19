import helpers
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import base64

def resetPassword(data):
    try:
        
        email = data["Email"]

        with open('private.pem', 'r') as f:
            private_key = f.read()
            
        private = RSA.importKey(private_key)
        cipher2 = Cipher_PKCS1_v1_5.new(private)

        byteString = cipher2.decrypt(base64.b64decode(email), "error")
        decryptedString = byteString.decode()


        arguments = (data["NewPassword"], decryptedString, data["OldPassword"], data["OldPassword"])
        helpers.masterCursor.execute("update Users set Password = SHA1(%s) where email = %s and (Password = SHA1(%s) or Password = %s)", arguments)

        arguments = (data["Email"], data["NewPassword"])
        helpers.masterCursor.execute("update Users set ResetPassword = 0 where email = %s and Password = SHA1(%s)", arguments)

        helpers.masterCursor.execute("update Users set AccountTypeFlag = 'General' where email = %s and Password = SHA1(%s)", arguments)
        helpers.masterDB.commit()
        return helpers.buildSuccessResponse("None")

    except:
        return helpers.buildErrorResponse("Unable to reset password. Please try again.")