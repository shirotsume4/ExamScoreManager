from models.dbengine.dbengine import SessionLocal
# Dependency
def get_db():
    try:
        db = SessionLocal()  # sessionを生成
        yield db
    finally:
        db.close()
    db.close()