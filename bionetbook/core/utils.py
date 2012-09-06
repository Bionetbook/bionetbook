def check_protocol_edit_authorization(protocol, user):

    if user.is_superuser or \
            user.is_staff or \
            user == protocol.owner:
        return True
    return False
