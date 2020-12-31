def get_user_id_from_info(info):
    try:
        return info.context.user_id
    except Exception:
        raise Exception('Authentication Failure!')
