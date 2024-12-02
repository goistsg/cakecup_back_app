from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.models.review_model import Review, ReviewCreate, ReviewUpdate

class ReviewRepository(ABC):
    @abstractmethod
    async def create_review(self, review: ReviewCreate) -> Review:
        pass

    @abstractmethod
    async def find_reviews(self) -> List[Review]:
        pass

    @abstractmethod
    async def find_reviews_by_product(self, product_id: str) -> List[Review]:
        pass

    @abstractmethod
    async def update_review(self, id: str, review: ReviewUpdate) -> Optional[Review]:
        pass

    @abstractmethod
    async def delete_review(self, id: str) -> bool:
        pass 