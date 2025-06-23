import bcrypt


def create_hash(plain_password: str) -> str:
    return  bcrypt.hashpw(
        password=plain_password.encode("utf-8"),
        salt=bcrypt.gensalt()
    ).decode(encoding="utf-8")


def verify_hash(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8")
    )
