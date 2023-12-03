from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# databaseの接続URL
SQLALCHEMY_DATABASE_URL = 'postgresql://fastapiuser:fastapipass@0.0.0.0:5432/fleamarket'

# databaseの接続エンジンを作成
# engineとはどのDBにどうやって接続をするかを設定を保持したオブジェクトでengineを通じてDB操作が行われる
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# DBセッションを管理
# bindはどのDBに接続するかの情報
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 新しいDBモデルを作成する際ベースとなるクラスを作成
# このBaseを継承することでそのクラスがsqlalchemyのmodelであると認識される
Base = declarative_base()

# DBのセッションを取得する関数
def get_db():
    db = Sessionlocal() # Sessionlocalを初期化
    try:
        yield db # return
    finally:
        db.close()