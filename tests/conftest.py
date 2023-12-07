import os, sys

# conftest.pyの一階層上の親ディレクトリを取得
app_dir = os.path.join(os.path.dirname(__file__), "..") 
sys.path.append(app_dir)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from models import Base, Item
from schermas  import DecodedToken
from main import app
from database import get_db
from cruds.auth import get_current_user


#test用のdbのセットアップを行うfixtureを定義する
@pytest.fixture()
def session_fixture():
# test用のDBの定義
    engine = create_engine(
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(engine) # modelsで定義したテーブルをsqliteで定義する

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

#テストデータの作成
    try:
        item1 = Item(name="PC1", price=10000, description="test1", user_id="1")
        item2 = Item(name="PC2", price=10000, description="test2", user_id="2")
        db.add(item1)
        db.add(item2)
        db.commit()
        yield db
    finally:
        db.close()

#test用のuserを定義
@pytest.fixture()
def user_fixture():
    return DecodedToken(username="user1", user_id=1)


@pytest.fixture()
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    def override_get_db():
        return session_fixture
    
    def override_get_current_user():
        return user_fixture
    
    # app内で使用指定たget_dbを今回定義したdbにオーバーライドする
    app.dependency_overrides[get_db] = override_get_db
    # ログイン認証を行なって使用するuser情報をテスト用の情報に上書きする
    app.dependency_overrides[get_current_user] = override_get_current_user


    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()
