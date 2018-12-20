from .models import Messages


class Create_table:
    def __init__(self):
        Messages.create_db()
