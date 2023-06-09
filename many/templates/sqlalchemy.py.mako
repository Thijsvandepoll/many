from sqlalchemy.orm import Session

version = ${repr(version)}
down_version = ${repr(down_version)}


def up(session: Session):
    # Insert your UP migration below
    ...


def down(session: Session):
    # Insert your DOWN migration below
    ...