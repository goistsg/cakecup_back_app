CREATE TYPE order_status AS ENUM (
    'pending',
    'processing',
    'paid',
    'cancelled',
    'delivered'
);

CREATE TYPE payment_status AS ENUM (
    'pending',
    'processing',
    'approved',
    'declined',
    'refunded'
);

CREATE TYPE payment_method AS ENUM (
    'credit_card',
    'pix',
    'bank_slip'
); 