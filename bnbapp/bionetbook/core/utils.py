def check_protocol_edit_authorization(protocol, user):

    #if protocol.status == protocol.STATUS_PUBLISHED:
    #    return False

    if user.is_superuser or \
            user.is_staff or \
            protocol.owner.pk in [ org.pk for org in user.organization_set.all() ]:
        return True
    return False
