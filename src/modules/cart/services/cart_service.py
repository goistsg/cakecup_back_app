from nest.core import Injectable
from typing import Optional, Dict, Any, List
from uuid import UUID
from fastapi import HTTPException
from src.modules.cart.repositories.cart_db_repository import CartDbRepository
from src.core.models.cart_model import Cart, CartStatus
from src.core.entity.cart_entity import CartEntity
from decimal import Decimal

@Injectable()
class CartService:
    def __init__(self, repository: CartDbRepository):
        self.repository = repository

    async def create_cart(self, user_id: UUID) -> Cart:
        try:
            cart_entity = await self.repository.create_cart(CartEntity(user_id=user_id))
            return Cart.from_entity(cart_entity)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao criar carrinho: {str(e)}")
    
    async def get_active_cart(self, user_id: UUID) -> Optional[Cart]:
        cart_entity = await self.repository.get_cart_active_and_by_user_id(user_id)
        if not cart_entity:
            cart_entity = await self.repository.create_cart(CartEntity(user_id=user_id, is_active=True, created_by=user_id))
        return Cart.from_entity(cart_entity)
    
    async def get_cart(self, cart_id: UUID) -> Optional[Cart]:
        cart_entity = await self.repository.get_cart_by_id(cart_id)
        if not cart_entity:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")
        return Cart.from_entity(cart_entity)
    
    async def add_item_to_cart(self, cart_id: UUID, item: Dict[str, Any], user_id: UUID) -> Cart:
        try:
            # Validação do item
            self._validate_item(item)

            # Busca o carrinho atual
            cart_entity = await self.repository.get_cart_by_id_and_user_id(cart_id, user_id)
            if not cart_entity:
                raise HTTPException(status_code=404, detail="Carrinho não encontrado")

            # Inicializa a lista de items se não existir
            cart_entity.items = cart_entity.items or []

            # Verifica se o item já existe no carrinho
            existing_item = next(
                (i for i in cart_entity.items if i.get('product_id') == item.get('product_id')), 
                None
            )

            if existing_item:
                # Atualiza a quantidade se o item já existe
                existing_item['quantity'] += item['quantity']
                # Atualiza o subtotal do item
                existing_item['subtotal'] = Decimal(str(existing_item['price'])) * existing_item['quantity']
            else:
                # Adiciona o subtotal ao novo item
                item['subtotal'] = Decimal(str(item['price'])) * item['quantity']
                # Adiciona o novo item ao carrinho
                cart_entity.items.append(item)

            # Recalcula o total do carrinho
            cart_entity.total = sum(
                Decimal(str(item.get('price', 0))) * item.get('quantity', 0) 
                for item in cart_entity.items
            )

            cart_entity.items = self._convert_decimals_to_float(cart_entity.items)

            # Atualiza o carrinho no banco de dados
            updated_cart = await self.repository.update_cart(cart_entity)
            
            return Cart.from_entity(updated_cart)

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Erro ao adicionar item ao carrinho: {str(e)}"
            )

    def _convert_decimals_to_float(self, items: list) -> list:
        """Converte todos os valores Decimal para float na lista de items"""
        converted_items = []
        for item in items:
            converted_item = item.copy()
            for key, value in converted_item.items():
                if isinstance(value, Decimal):
                    converted_item[key] = float(value)
            converted_items.append(converted_item)
        return converted_items

    def _validate_item(self, item: Dict[str, Any]) -> None:
        """Valida os dados do item antes de adicionar ao carrinho"""
        required_fields = {
            'product_id': 'ID do produto é obrigatório',
            'name': 'Nome do produto é obrigatório',
            'price': 'Preço é obrigatório',
            'quantity': 'Quantidade é obrigatória'
        }

        # Verifica campos obrigatórios
        for field, message in required_fields.items():
            if field not in item:
                raise HTTPException(status_code=400, detail=message)

        # Valida quantidade
        if item['quantity'] <= 0:
            raise HTTPException(
                status_code=400, 
                detail="Quantidade deve ser maior que zero"
            )

        # Valida preço
        try:
            price = Decimal(str(item['price']))
            if price <= 0:
                raise HTTPException(
                    status_code=400, 
                    detail="Preço deve ser maior que zero"
                )
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=400, 
                detail="Preço inválido"
            )
    
    async def remove_item_from_cart(self, cart_id: UUID, product_id: str, user_id: UUID) -> Cart:
        try:
            cart_entity = await self.repository.get_cart_by_id_and_user_id(cart_id, user_id)
            if not cart_entity:
                raise HTTPException(status_code=404, detail="Carrinho não encontrado")

            if not cart_entity.items:
                raise HTTPException(status_code=404, detail="Carrinho está vazio")

            # Procura o item no carrinho
            item_index = next(
                (index for (index, item) in enumerate(cart_entity.items) 
                if item.get('product_id') == product_id),
                None
            )

            if item_index is None:
                raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")

            # Remove o item da lista
            removed_item = cart_entity.items.pop(item_index)
            print(f"Item removido: {removed_item}")  # Debug

            # Atualiza a lista de items e recalcula subtotais
            updated_items = []
            total = Decimal('0')

            for item in cart_entity.items:
                subtotal = Decimal(str(item['price'])) * item['quantity']
                item['subtotal'] = float(subtotal)
                total += subtotal
                updated_items.append(item)

            # Atualiza o carrinho
            cart_entity.items = updated_items
            cart_entity.total = float(total)

            print(f"Items atualizados: {cart_entity.items}")  # Debug
            print(f"Total atualizado: {cart_entity.total}")   # Debug

            # Atualiza o carrinho no banco
            updated_cart = await self.repository.update_cart(cart_entity)
            
            return Cart.from_entity(updated_cart)

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Erro ao remover item do carrinho: {str(e)}"
            )
    
    async def update_item_quantity(self, cart_id: UUID, product_id: str, quantity: int, user_id: UUID) -> Cart:
        try:
            # Validação básica da quantidade
            if quantity <= 0:
                raise HTTPException(
                    status_code=400, 
                    detail="Quantidade deve ser maior que zero"
                )

            # Busca o carrinho
            cart_entity = await self.repository.get_cart_by_id_and_user_id(cart_id, user_id)
            if not cart_entity:
                raise HTTPException(status_code=404, detail="Carrinho não encontrado")

            # Verifica se o carrinho tem items
            if not cart_entity.items:
                raise HTTPException(status_code=404, detail="Carrinho está vazio")

            # Procura o item no carrinho
            item_index = next(
                (index for (index, item) in enumerate(cart_entity.items) 
                if item.get('product_id') == product_id),
                None
            )

            if item_index is None:
                raise HTTPException(status_code=404, detail="Item não encontrado no carrinho")

            # Atualiza a quantidade do item
            cart_entity.items[item_index]['quantity'] = quantity
            
            # Recalcula o subtotal do item
            price = Decimal(str(cart_entity.items[item_index]['price']))
            cart_entity.items[item_index]['subtotal'] = float(price * quantity)

            # Recalcula o total do carrinho
            cart_entity.total = float(sum(
                Decimal(str(item['price'])) * item['quantity']
                for item in cart_entity.items
            ))

            print(f"Item atualizado: {cart_entity.items[item_index]}")  # Debug
            print(f"Total atualizado: {cart_entity.total}")  # Debug

            # Atualiza o carrinho no banco
            updated_cart = await self.repository.update_cart(cart_entity)
            
            return Cart.from_entity(updated_cart)

        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Erro ao atualizar quantidade: {str(e)}")  # Debug
            raise HTTPException(
                status_code=400, 
                detail=f"Erro ao atualizar quantidade do item: {str(e)}"
            )

    async def clear_cart(self, cart_id: UUID, user_id: UUID) -> Cart:
        try:
            # Busca o carrinho
            cart_entity = await self.repository.get_cart_by_id_and_user_id(cart_id, user_id)
            if not cart_entity:
                raise HTTPException(status_code=404, detail="Carrinho não encontrado")

            # Limpa os items e zera o total
            cart_entity.items = []
            cart_entity.total = 0.0

            # Atualiza o carrinho no banco
            updated_cart = await self.repository.update_cart(cart_entity)
            print(f"Carrinho limpo: {updated_cart}")  # Debug
            
            return Cart.from_entity(updated_cart)

        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Erro ao limpar carrinho: {str(e)}")  # Debug
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao limpar carrinho: {str(e)}"
            )
    
    async def get_user_cart(self, user_id: UUID) -> Optional[List[Cart]]:
        cart_entity = await self.repository.get_cart_by_user_id(user_id)
        if not cart_entity:
            raise HTTPException(status_code=404, detail="Carrinho não encontrado")
        return [Cart.from_entity(cart) for cart in cart_entity]

    async def close_cart(self, cart_id) -> Cart:
        try:
            cart_entity = await self.repository.get_cart_by_id(cart_id)
            if not cart_entity:
                raise HTTPException(status_code=404, detail="Carrinho não encontrado")
            cart_entity.status = CartStatus.CLOSED
            cart_entity.is_active = False

            updated_cart = await self.repository.close_cart(cart_entity)
            print(f"Carrinho fechado: {updated_cart}")
            
            return Cart.from_entity(updated_cart)

        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Erro ao fechar carrinho: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao fechar carrinho: {str(e)}"
            )
