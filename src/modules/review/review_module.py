from nest.core import Module
from src.modules.review.services.review_service import ReviewService
from src.modules.review.repositories.review_db_repository import ReviewDbRepository

@Module(
    controllers=[],
    providers=[
        ReviewService,
        ReviewDbRepository
    ]
)
class ReviewModule:
    pass 