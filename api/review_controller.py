from nest.core import Controller, Get, Post, Patch, Delete
from typing import List
from src.core.models.review_model import Review, ReviewCreate, ReviewUpdate
from src.modules.review.services.review_service import ReviewService
from src.core.providers.response_handler import ResponseHandler, ApiResponse

@Controller("/reviews", tag=["Avaliações"])
class ReviewController:
    def __init__(self, service: ReviewService, response_handler: ResponseHandler):
        self.service = service
        self.response_handler = response_handler

    @Post()
    async def create_review(self, review: ReviewCreate) -> ApiResponse[Review]:
        try:
            created = await self.service.create_review(review)
            return self.response_handler.wrap_response(
                data=created,
                message="Avaliação criada com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao criar avaliação",
                errors=str(e)
            )

    @Get("/product/{product_id}")
    async def find_reviews_by_product(self, product_id: str) -> ApiResponse[List[Review]]:
        try:
            reviews = await self.service.find_reviews_by_product(product_id)
            return self.response_handler.wrap_response(
                data=reviews,
                message="Avaliações recuperadas com sucesso"
            )
        except Exception as e:
            return self.response_handler.wrap_error(
                message="Erro ao buscar avaliações",
                errors=str(e)
            ) 