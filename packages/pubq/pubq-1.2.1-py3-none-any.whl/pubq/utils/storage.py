import dbm


class storage:

    def __init__(self):
        self.db_name = 'pubq_auth_tokens'

    def set(self, key, value):
        try:
            # Ensure the token is encoded to bytes
            value_bytes = value.encode('utf-8')

            # Open (or create) a dbm database
            with dbm.open(self.db_name, 'c') as db:
                # Storing the token string
                db[key] = value_bytes
        except FileNotFoundError:
            # Handle the case when the database file doesn't exist
            print("Database file not found.")
            return None
        except Exception as e:
            # Handle other exceptions gracefully
            print("Error:", e)
            return None

    def get(self, key):
        try:
            with dbm.open(self.db_name, 'r') as db:
                value_bytes = db.get(key.encode('utf-8'))
                if value_bytes is not None:
                    return value_bytes.decode('utf-8')
                else:
                    return None
        except FileNotFoundError:
            # Handle the case when the database file doesn't exist
            print("Database file not found.")
            return None
        except Exception as e:
            # Handle other exceptions gracefully
            print("Error:", e)
            return None

    def remove(self, key):
        try:
            with dbm.open(self.db_name, 'w') as db:
                db[key] = None
        except FileNotFoundError:
            # Handle the case when the database file doesn't exist
            print("Database file not found.")
            return None
        except Exception as e:
            # Handle other exceptions gracefully
            print("Error:", e)
            return None

    def clear(self):
        try:
            with dbm.open(self.db_name, 'w') as db:
                db.clear()
        except FileNotFoundError:
            # Handle the case when the database file doesn't exist
            print("Database file not found.")
            return None
        except Exception as e:
            # Handle other exceptions gracefully
            print("Error:", e)
            return None
