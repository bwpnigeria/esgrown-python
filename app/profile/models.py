from typing import Any
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
)

from app.mixins.columns import BaseModelMixin
from app.config.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

class Profile(BaseModelMixin, Base):
    user_id = Column(String(45), ForeignKey("users.uuid"), nullable=False)
    state_id = Column(String(45), ForeignKey("states.uuid"), nullable=True)
    lga_id = Column(String(45), ForeignKey("localgovernments.uuid"), nullable=True)
    address = Column(String(255), nullable=True)
    date_of_birth = Column(String(45), nullable=True)
    gender = Column(String(16), nullable=True)
    photo = Column(String(255), nullable=True)
    state: Any = relationship("State", lazy="joined", foreign_keys=[state_id])
    lga: Any = relationship("LocalGovernment", lazy="joined", foreign_keys=[lga_id])
    user: Any = relationship("User", lazy="joined", foreign_keys=[user_id])

    @declared_attr
    def creator(cls: Any) -> Any:
        return relationship("User", lazy="joined", foreign_keys=[cls.created_by])
    