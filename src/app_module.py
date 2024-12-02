from nest.core import PyNestFactory, Module
from src.modules.user.user_module import UserModule
from src.core.providers.response_handler import ResponseHandler
from src.core.providers.async_orm_provider import AsyncOrmProvider
from src.core.middleware.response_middleware import ResponseMiddleware
from src.core.middleware.cors_middleware import CorsMiddleware
from src.modules.cart.cart_module import CartModule
from src.modules.payments.payment_module import PaymentModule
from src.modules.product.product_module import ProductModule
from src.modules.user.user_module import UserModule
from src.modules.orders.order_module import OrderModule
from api.auth_controller import AuthController
from api.user_controller import UserController
from api.cart_controller import CartController
from api.product_controller import ProductController
from api.order_controller import OrderController

@Module(
    imports=[
        CartModule,
        PaymentModule,
        ProductModule,
        UserModule,
        OrderModule,
    ],
    controllers=[
        AuthController,
        CartController,
        ProductController,
        UserController,
        OrderController
    ],
    providers=[
        AsyncOrmProvider,
        ResponseHandler,
        ResponseMiddleware
    ],
    exports=[ResponseHandler]
)
class AppModule:
    pass

app = PyNestFactory.create(
    AppModule,
    title="CakeCup API",
    description="""
    API do CakeCup - Sistema de Pedidos de Cupcakes
    
    ## Funcionalidades
    
    * 👤 Autenticação e Gestão de Usuários
    * 🧁 Catálogo de Produtos
    * 🛒 Carrinho de Compras
    * 📦 Gestão de Pedidos
    * 💳 Processamento de Pagamentos
    * ⭐ Sistema de Avaliações
    """,
    version="1.0.0",
    contact={
        "name": "Tiago Soares de Gois",
        "url": "https://github.com/goistsg"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

http_server = app.get_server()

http_server.add_middleware(
    CorsMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True
)
