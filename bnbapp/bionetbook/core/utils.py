def check_protocol_edit_authorization(protocol, user):

    if protocol.status == protocol.STATUS_PUBLISHED:
        return False

    if user.is_superuser or \
            user.is_staff or \
            user == protocol.owner:
        return True
    return False
