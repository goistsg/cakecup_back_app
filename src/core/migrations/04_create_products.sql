CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INTEGER NOT NULL DEFAULT 0,
    sku VARCHAR(100) UNIQUE,
    is_active BOOLEAN DEFAULT true,
    image_url TEXT,
    
    flavor VARCHAR(100) NOT NULL,
    frosting_type VARCHAR(100),
    decoration_description TEXT,
    is_gluten_free BOOLEAN DEFAULT false,
    is_lactose_free BOOLEAN DEFAULT false,
    is_vegan BOOLEAN DEFAULT false,
    allergens TEXT[],
    ingredients TEXT NOT NULL,
    size VARCHAR(20) DEFAULT 'regular',
    calories INTEGER,
    
    created_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER update_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE INDEX idx_products_flavor ON products(flavor);
CREATE INDEX idx_products_is_active ON products(is_active);
CREATE INDEX idx_products_dietary_options ON products(is_gluten_free, is_lactose_free, is_vegan);
CREATE INDEX idx_products_size ON products(size); 