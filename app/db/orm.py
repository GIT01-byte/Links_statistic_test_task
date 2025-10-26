
from sqlalchemy import and_, select
from db.session import Base, async_engine, async_session_factory
from models.links import LinksOrm
from schemas.links import LinksDTO


class AsyncOrm:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def get_all_links(limit: int, offset: int):
        async with async_session_factory() as session:
            query = select(
                LinksOrm
                ).limit(
                    limit
                    ).offset(
                        offset
                        )
            
            res = await session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")

            result_dto = [LinksDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def get_all_domain_with_timestamp(time_from: int, time_to: int, limit: int, offset: int):
        async with async_session_factory() as session:
            query = select(
                LinksOrm
                ).where(
                and_(
                    LinksOrm.timestamp >= time_from,
                    LinksOrm.timestamp <= time_to,
                    )
                ).distinct(
                    LinksOrm.link
                    ).limit(
                        limit
                        ).offset(
                            offset
                            )
            
            res = await session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")

            result_dto = [LinksDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto

    @staticmethod
    async def add_link(link: LinksOrm):
        async with async_session_factory() as session:
            session.add(link)
            await session.flush()
            await session.commit()

