def check_token(token: str) -> bool:
    if not token:
        raise ValueError('Bot token is undefined! Use init()')
    return True
