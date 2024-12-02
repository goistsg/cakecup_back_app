from nest.core import Injectable
from typing import List
from sqlalchemy import select
from uuid_extensions import uuid7
from src.modules.review.repositories.review_repository import ReviewRepository
from src.core.models.review_model import Review, ReviewCreate
from src.core.entity.review_entity import ReviewEntity
from src.core.providers.async_orm_provider import AsyncOrmProvider

@Injectable()
class ReviewDbRepository(ReviewRepository):
    def __init__(self, orm_provider: AsyncOrmProvider):
        self.orm_provider = orm_provider

    async def create_review(self, review: ReviewCreate) -> Review:
        try:
            session = await self.orm_provider.get_session()
            try:
                review_entity = ReviewEntity(
                    id=str(uuid7()),
                    product_id=review.product_id,
                    user_id=review.user_id,
                    rating=review.rating,
                    comment=review.comment
                )
                
                session.add(review_entity)
                await session.commit()
                await session.refresh(review_entity)
                
                return Review.from_orm(review_entity)
            finally:
                await session.close()
        except Exception as e:
            print(f"Erro ao criar avaliação: {str(e)}")
            raise e

    async def find_reviews_by_product(self, product_id: str) -> List[Review]:
        try:
            session = await self.orm_provider.get_session()
            try:
                result = await session.execute(
                    select(ReviewEntity).where(ReviewEntity.product_id == product_id)
                )
                reviews = result.scalars().all()
                return [Review.from_orm(review) for review in reviews]
            finally:
                await session.close()
        except Exception as e:
            print(f"Erro ao buscar avaliações: {str(e)}")
            return []

    async def find_reviews(self) -> List[Review]:
        try:
            session = await self.orm_provider.get_session()
            try:
                result = await session.execute(select(ReviewEntity))
                reviews = result.scalars().all()
                return [Review.from_orm(review) for review in reviews]
            finally:
                await session.close()
        except Exception as e:
            print(f"Erro ao buscar todas as avaliações: {str(e)}")
            return []

    async def update_review(self, review_id: str, review_data: ReviewCreate) -> Review:
        try:
            session = await self.orm_provider.get_session()
            try:
                result = await session.execute(
                    select(ReviewEntity).where(ReviewEntity.id == review_id)
                )
                review_entity = result.scalar_one_or_none()
                
                if not review_entity:
                    raise Exception("Avaliação não encontrada")

                review_entity.rating = review_data.rating
                review_entity.comment = review_data.comment
                
                await session.commit()
                await session.refresh(review_entity)
                
                return Review.from_orm(review_entity)
            finally:
                await session.close()
        except Exception as e:
            print(f"Erro ao atualizar avaliação: {str(e)}")
            raise e

    async def delete_review(self, review_id: str) -> bool:
        try:
            session = await self.orm_provider.get_session()
            try:
                result = await session.execute(
                    select(ReviewEntity).where(ReviewEntity.id == review_id)
                )
                review_entity = result.scalar_one_or_none()
                
                if not review_entity:
                    return False

                await session.delete(review_entity)
                await session.commit()
                
                return True
            finally:
                await session.close()
        except Exception as e:
            print(f"Erro ao deletar avaliação: {str(e)}")
            return False 