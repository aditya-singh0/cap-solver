import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.database import User, APIKey

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = "HS256"
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.PyJWTError:
            return None
    
    def generate_api_key(self) -> str:
        """Generate a new API key"""
        return f"cap_{secrets.token_urlsafe(32)}"
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash API key for storage"""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def verify_api_key(self, api_key: str, db: Session) -> Optional[APIKey]:
        """Verify API key and return the key object"""
        if not api_key.startswith("cap_"):
            return None
        
        key_hash = self.hash_api_key(api_key)
        db_key = db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.is_active == True
        ).first()
        
        if db_key:
            # Update last used timestamp
            db_key.last_used_at = datetime.utcnow()
            db.commit()
            return db_key
        
        return None
    
    def create_user(self, db: Session, email: str, password: str) -> User:
        """Create a new user"""
        hashed_password = self.get_password_hash(password)
        db_user = User(
            email=email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_api_key(self, db: Session, user_id: int, name: str) -> tuple[str, APIKey]:
        """Create a new API key for a user"""
        api_key = self.generate_api_key()
        key_hash = self.hash_api_key(api_key)
        
        db_api_key = APIKey(
            key_hash=key_hash,
            name=name,
            user_id=user_id
        )
        db.add(db_api_key)
        db.commit()
        db.refresh(db_api_key)
        
        return api_key, db_api_key
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first() 