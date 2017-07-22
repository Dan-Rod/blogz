def validate_user(email, password, password_verify):
    error = {}
    #error[email_error]=''
    #error[password_error]=''
    #error[password_verify_error]=''
    

    

    if not " " in email:
        if len(email) >= 3 and len(email) <= 20:
            if "@" in email and "." in email:
                error['email_error'] = ''
            else:
                error['email_error'] = "Email must contain '@' and '.' to be valid. Please try again!"
        else:
            error['email_error'] = "Email must contain '@' and '.' to be valid. Please try again!"
    else:
        error['email_error'] = "Email must contain '@' and '.' to be valid. Please try again!"


    if not " " in password:
        if len(password) < 3 or len(email) > 20:
            error[password_error] = "Password must be between 3 and 20 characters with no spaces. Please try again!"
    else:
        error[password_error] = "Password must be between 3 and 20 characters with no spaces. Please try again!" 
    
    if password != password_verify:
        error[password_verify_error] = "Passwords do not match."

   
    if error['email_error']:
        return error['email_error']
    elif error['password_error']:
        return error['password_error']
    elif error['password_verify_error']:
        return error['password_verify_error']
    else:
        return  True