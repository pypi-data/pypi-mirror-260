def get_win_info(entry):
    # Thanks to Wendel at https://stackoverflow.com/questions/71018167/get-owner-of-a-file-using-python-on-windows-system
    try:
        import win32security
        sd = win32security.GetFileSecurity(str(entry), win32security.OWNER_SECURITY_INFORMATION)
        owner_sid = sd.GetSecurityDescriptorOwner()
        name, domain, tpe = win32security.LookupAccountSid(None, owner_sid)
        return name, domain
    except:
        return None, None