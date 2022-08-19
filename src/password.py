import helpers


def resetPassword(data):
    try:
        print(data)
        arguments = (data["NewPassword"], data["Email"], data["OldPassword"], data["OldPassword"])
        helpers.masterCursor.execute("update Users set Password = SHA1(%s) where email = %s and (Password = SHA1(%s) or Password = %s)", arguments)

        arguments = (data["Email"], data["NewPassword"])
        helpers.masterCursor.execute("update Users set ResetPassword = 0 where email = %s and Password = SHA1(%s)", arguments)

        helpers.masterCursor.execute("update Users set AccountTypeFlag = 'General' where email = %s and Password = SHA1(%s)", arguments)
        helpers.masterDB.commit()
        return helpers.buildSuccessResponse("None")

    except:
        return helpers.buildErrorResponse("Unable to reset password. Please try again.")