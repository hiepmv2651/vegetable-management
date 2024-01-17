from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship, backref
from app.core.database import Base


class TimestampMixin:
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class IdMixin:
    id = Column(Integer, primary_key=True, index=True)


class Role(Base, IdMixin, TimestampMixin):
    __tablename__ = "roles"

    role_name = Column(String(50), unique=True, index=True)


class Users(Base, IdMixin, TimestampMixin):
    __tablename__ = "users"

    username = Column(String(50), unique=True, index=True)
    password = Column(String(255))
    email = Column(Text, unique=True, index=True)
    full_name = Column(String(50))
    phone_number = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))

    role = relationship("Role", backref=backref("users", cascade="all, delete-orphan"))


class Employees(Base, IdMixin, TimestampMixin):
    __tablename__ = "employees"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    position = Column(String(50))
    contact_number = Column(String(50))
    salary = Column(Integer)
    hire_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    user = relationship(
        "Users", backref=backref("employees", cascade="all, delete-orphan")
    )


class Categories(Base, IdMixin, TimestampMixin):
    __tablename__ = "categories"

    name = Column(String(50), unique=True, index=True)


class Products(Base, IdMixin, TimestampMixin):
    __tablename__ = "products"

    name = Column(String(50), unique=True, index=True)
    price = Column(Integer)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    stock_quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    category = relationship(
        "Categories", backref=backref("products", cascade="all, delete-orphan")
    )


class Reviews(Base, IdMixin, TimestampMixin):
    __tablename__ = "reviews"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    rating = Column(Integer)
    comment = Column(String(50))

    user = relationship(
        "Users", backref=backref("reviews", cascade="all, delete-orphan")
    )
    product = relationship(
        "Products", backref=backref("reviews", cascade="all, delete-orphan")
    )


class Conversations(Base, IdMixin, TimestampMixin):
    __tablename__ = "conversations"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"))

    user = relationship(
        "Users", backref=backref("conversations", cascade="all, delete-orphan")
    )
    employee = relationship(
        "Employees", backref=backref("conversations", cascade="all, delete-orphan")
    )


class Messages(Base, IdMixin, TimestampMixin):
    __tablename__ = "messages"

    conversation_id = Column(
        Integer, ForeignKey("conversations.id", ondelete="CASCADE")
    )
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(Text)

    conversation = relationship(
        "Conversations", backref=backref("messages", cascade="all, delete-orphan")
    )
    user = relationship(
        "Users", backref=backref("messages", cascade="all, delete-orphan")
    )


class Orders(Base, IdMixin, TimestampMixin):
    __tablename__ = "orders"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    order_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    total_price = Column(Integer)
    delivery_address = Column(Text)
    payment_method = Column(String(50))
    status = Column(String(50))

    user = relationship(
        "Users", backref=backref("orders", cascade="all, delete-orphan")
    )


class OrderDetails(Base, IdMixin, TimestampMixin):
    __tablename__ = "order_details"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer)
    sub_total = Column(Integer)

    order = relationship(
        "Orders", backref=backref("order_details", cascade="all, delete-orphan")
    )
    product = relationship(
        "Products", backref=backref("order_details", cascade="all, delete-orphan")
    )


class Emails(Base, IdMixin, TimestampMixin):
    __tablename__ = "emails"

    sender_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    subject = Column(String(50))
    content = Column(Text)

    user = relationship(
        "Users", backref=backref("emails", cascade="all, delete-orphan")
    )
    
    employee = relationship(
        "Employees", backref=backref("emails", cascade="all, delete-orphan")
    )


class Contacts(Base, IdMixin, TimestampMixin):
    __tablename__ = "contacts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    subject = Column(String(50))
    message = Column(Text)

    user = relationship(
        "Users", backref=backref("contacts", cascade="all, delete-orphan")
    )


class DeliveryMaps(Base, IdMixin, TimestampMixin):
    __tablename__ = "delivery_maps"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    map_url = Column(Text)

    order = relationship(
        "Orders", backref=backref("delivery_maps", cascade="all, delete-orphan")
    )


class Invoices(Base, IdMixin, TimestampMixin):
    __tablename__ = "invoices"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    total_price = Column(Integer)
    issued_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    order = relationship(
        "Orders", backref=backref("invoices", cascade="all, delete-orphan")
    )


class QRCodes(Base, IdMixin, TimestampMixin):
    __tablename__ = "qrcodes"

    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"))
    qrcode_url = Column(String(50))

    invoice = relationship(
        "Invoices", backref=backref("qrcodes", cascade="all, delete-orphan")
    )


class Payments(Base, IdMixin, TimestampMixin):
    __tablename__ = "payments"

    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    payment_amount = Column(Integer)
    payment_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    payment_status = Column(String(50))

    order = relationship(
        "Orders", backref=backref("payments", cascade="all, delete-orphan")
    )


class DiscountCodes(Base, IdMixin, TimestampMixin):
    __tablename__ = "discount_codes"

    code = Column(String(50), unique=True, index=True)
    discount_percentage = Column(Integer)
    discount_amount = Column(Integer)
    expiry_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    single_use = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    start_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    end_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    is_active = Column(Boolean, default=False)

    user = relationship(
        "Users", backref=backref("discount_codes", cascade="all, delete-orphan")
    )


class Permissions(Base, IdMixin, TimestampMixin):
    __tablename__ = "permissions"

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"))
    permission_name = Column(String(50), unique=True, index=True)
    description = Column(Text, nullable=True)

    role = relationship(
        "Role", backref=backref("permissions", cascade="all, delete-orphan")
    )


class Statistics(Base, IdMixin, TimestampMixin):
    __tablename__ = "statistics"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    order_count = Column(Integer)
    total_revenue = Column(Integer)
    review_count = Column(Integer)

    user = relationship(
        "Users", backref=backref("statistics", cascade="all, delete-orphan")
    )


class Carts(Base, IdMixin, TimestampMixin):
    __tablename__ = "carts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer)

    user = relationship(
        "Users", backref=backref("carts", cascade="all, delete-orphan")
    )
    product = relationship(
        "Products", backref=backref("carts", cascade="all, delete-orphan")
    )