class SessionManager:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            # No exceptions, so commit the transaction
            self.session.commit()
        else:
            # Exception occurred, so rollback the transaction
            self.session.rollback()
        self.session.close()
