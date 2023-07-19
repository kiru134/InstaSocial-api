from database import Base, engine


def init_db():

    Base.metadata.create_all(bind=engine)
    print("Initialized the db")


if __name__ == "__main__":
    init_db()