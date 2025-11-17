import pandas as pd
from sqlalchemy import Column, Date, Float, String, create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import Config

Base = declarative_base()


class YieldCurvePoint(Base):
    __tablename__ = "yield_curve_points"

    id = Column(String, primary_key=True)  # e.g. "2023-01-02_UST_2.0"
    date = Column(Date, index=True)
    curve_name = Column(String, index=True, default="UST")
    tenor_years = Column(Float)
    yield_value = Column(Float)

    __table_args__ = (
        UniqueConstraint("date", "curve_name", "tenor_years", name="uix_curve_point"),
    )


def create_session(config: Config):
    engine = create_engine(config.db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def df_to_db(
    df: pd.DataFrame,
    curve_name: str,
    config: Config,
) -> None:
    """
    Persist curve DataFrame to DB. df must have: ['date', 'tenor_years', 'yield'].
    """
    session = create_session(config)
    try:
        for _, row in df.iterrows():
            date = row["date"].date()
            tenor = float(row["tenor_years"])
            yld = float(row["yield"])   

            cid = f"{date.isoformat()}_{curve_name}_{tenor}"
            obj = YieldCurvePoint(
                id=cid,
                date=date,
                curve_name=curve_name,
                tenor_years=tenor,
                yield_value=yld,
            )
            session.merge(obj)  # upsert
        session.commit()
    finally:
        session.close()


def load_curve_timeseries(
    config: Config,
    curve_name: str = "UST",
) -> pd.DataFrame:
    """
    Load all stored curve points into a long DataFrame.
    """
    session = create_session(config)
    try:
        q = (
            session.query(YieldCurvePoint)
            .filter(YieldCurvePoint.curve_name == curve_name)
        )
        rows = q.all()
    finally:
        session.close()

    data = [
        {
            "date": r.date,
            "curve_name": r.curve_name,
            "tenor_years": r.tenor_years,
            "yield": r.yield_value,
        }
        for r in rows
    ]
    df = pd.DataFrame(data)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df.sort_values(["date", "tenor_years"])
