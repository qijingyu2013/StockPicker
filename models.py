import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

from sqlalchemy import (
    create_engine,
    Column,
    BigInteger,
    Integer,
    Float,
    String,
    Text,
    Enum,
    DECIMAL,
    DateTime,
    Boolean,
    UniqueConstraint,
    Index
)
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URI

# 基础类
Base = declarative_base()

# 创建引擎
engine = create_engine(
    DB_URI,
    # 超过链接池大小外最多创建的链接
    max_overflow=0,
    # 链接池大小
    pool_size=5,
    # 链接池中没有可用链接则最多等待的秒数，超过该秒数后报错
    pool_timeout=10,
    # 多久之后对链接池中的链接进行一次回收
    pool_recycle=1,
    # 查看原生语句（未格式化）
    echo=False
)

# 绑定引擎
Session = sessionmaker(bind=engine)
# 创建数据库链接池，直接使用session即可为当前线程拿出一个链接对象conn
# 内部会采用threading.local进行隔离
session = scoped_session(Session)


class StockList(Base):
    # """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "stock_list"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    name = Column(String(10), index=True, nullable=False, comment="股票名称")
    code = Column(String(8), nullable=True, comment="股票代码")
    flag = Column(String(2), nullable=True, comment="标志位 SZ , SH")
    status = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ，  其他1")
    delete = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ， 删除1")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")


class StockTrade(Base):
    # """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "stock_trade"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    sid = Column(Integer, comment="stock_list的主键")
    name = Column(String(10), index=True, nullable=False, comment="股票名称")
    code = Column(String(8), nullable=True, comment="股票代码")
    timestamp = Column(BigInteger, nullable=True, comment="交易日时间戳")
    volume = Column(Integer, nullable=True, comment="成交量(手)")
    open = Column(Float, nullable=True, comment="开盘价")
    high = Column(Float, nullable=True, comment="最高价")
    low = Column(Float, nullable=True, comment="最低价")
    close = Column(Float, nullable=True, comment="收盘价")
    chg = Column(Float, nullable=True, comment="涨跌幅")
    percent = Column(Float, nullable=True, comment="涨跌幅%")
    turn_over_rate = Column(Float, nullable=True, comment="换手率%")
    amount = Column(Float, nullable=True, comment="成交额")
    limit_up = Column(Float, nullable=True, comment="涨停价")
    limit_down = Column(Float, nullable=True, comment="跌停价")
    status = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ，  其他1")
    delete = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ， 删除1")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")


class StockDistribution(Base):
    # """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "stock_distribution"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    sid = Column(Integer, comment="stock_list的主键")
    name = Column(String(10), index=True, nullable=False, comment="股票名称")
    code = Column(String(8), nullable=True, comment="股票代码")
    timestamp = Column(BigInteger, nullable=True, comment="交易日时间戳")
    datas = Column(Text, nullable=True, comment="筹码分布数据")
    delete = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ， 删除1")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")


class StockMission(Base):
    # """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "stock_mission"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    timestamp = Column(BigInteger, nullable=True, comment="时间戳")  # 时间戳
    type = Column(Integer, comment="任务类型 1=倍量 2=9日阴 3=9周阴 4=9月阴 5=放量 6=底部筹码 7=倍量横盘")
    content = Column(Text, nullable=True, comment="执行结果")
    delete = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ， 删除1")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")


class StockTradeWeekly(Base):
    # """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "stock_trade_weekly"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    sid = Column(Integer, comment="stock_list的主键")
    name = Column(String(10), index=True, nullable=False, comment="股票名称")
    code = Column(String(8), nullable=True, comment="股票代码")
    timestamp = Column(BigInteger, nullable=True, comment="交易日时间戳")
    volume = Column(Integer, nullable=True, comment="成交量(手)")
    open = Column(Float, nullable=True, comment="开盘价")
    high = Column(Float, nullable=True, comment="最高价")
    low = Column(Float, nullable=True, comment="最低价")
    close = Column(Float, nullable=True, comment="收盘价")
    chg = Column(Float, nullable=True, comment="涨跌幅")
    percent = Column(Float, nullable=True, comment="涨跌幅%")
    turn_over_rate = Column(Float, nullable=True, comment="换手率%")
    amount = Column(Float, nullable=True, comment="成交额")
    status = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ，  其他1")
    delete = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ， 删除1")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")


class StockTradeMonthly(Base):
    # """ 必须继承Base """
    # 数据库中存储的表名
    __tablename__ = "stock_trade_monthly"
    # 对于必须插入的字段，采用nullable=False进行约束，它相当于NOT NULL
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="主键")
    sid = Column(Integer, comment="stock_list的主键")
    name = Column(String(10), index=True, nullable=False, comment="股票名称")
    code = Column(String(8), nullable=True, comment="股票代码")
    timestamp = Column(BigInteger, nullable=True, comment="交易日时间戳")
    volume = Column(Integer, nullable=True, comment="成交量(手)")
    open = Column(Float, nullable=True, comment="开盘价")
    high = Column(Float, nullable=True, comment="最高价")
    low = Column(Float, nullable=True, comment="最低价")
    close = Column(Float, nullable=True, comment="收盘价")
    chg = Column(Float, nullable=True, comment="涨跌幅")
    percent = Column(Float, nullable=True, comment="涨跌幅%")
    turn_over_rate = Column(Float, nullable=True, comment="换手率%")
    amount = Column(Float, nullable=True, comment="成交额")
    status = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ，  其他1")
    delete = Column(DECIMAL(1), default=0, comment="是否删除  默认0 ， 删除1")
    create_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = Column(DateTime, onupdate=datetime.datetime.now, comment="最后更新时间")


__table__args__ = (
    UniqueConstraint("name", "code", "flag"),  # 联合唯一约束
    Index("code", "flag", unique=True),  # 联合唯一索引
)


def __str__(self):
    return f"object : <id:{self.id} name:{self.name}>"


if __name__ == "__main__":
    # 删除表
    Base.metadata.drop_all(engine)
    # 创建表
    Base.metadata.create_all(engine)
