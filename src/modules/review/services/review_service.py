from nest.core import Injectable
from typing import List, Optional
from ....core.models.review_model import Review, ReviewCreate, ReviewUpdate
from ..repositories.review_db_repository import ReviewDbRepository
from uuid import UUID

@Injectable()
class ReviewService:
    def __init__(self, review_repository: ReviewDbRepository):
        self.review_repository = review_repository

    async def create_review(self, review: ReviewCreate) -> Review:
        try:
            if isinstance(review.product_id, str):
                review.product_id = UUID(review.product_id)
            if isinstance(review.user_id, str):
                review.user_id = UUID(review.user_id)
                
            return await self.review_repository.create_review(review)
        except Exception as e:
            raise Exception(f"Erro ao criar avaliação: {str(e)}")

    async def find_reviews_by_product(self, product_id: str) -> List[Review]:
        return await self.review_repository.find_reviews_by_product(product_id)

    async def update_review(self, id: str, review: ReviewUpdate) -> Optional[Review]:
        return await self.review_repository.update_review(id, review)

    async def delete_review(self, id: str) -> bool:
        return await self.review_repository.delete_review(id) 