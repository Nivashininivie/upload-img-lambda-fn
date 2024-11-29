import jwt

class JwtDecoderForUserId:

    @staticmethod
    def decode_token(event):
        """Extract and decode JWT token from the Authorization header."""
        authorization_header = event.get('headers', {}).get('Authorization', None)
        
        if not authorization_header:
            raise Exception("Authorization header is missing")
        
        # The token should be in the format: Bearer <access-token>
        token = authorization_header.split(' ')[1] if authorization_header.startswith('Bearer ') else None
        
        if not token:
            raise Exception("Invalid Authorization header format")
        
        try:
            # Decode the JWT token without verification (no signature check)
            payload = jwt.decode(token, options={"verify_signature": False})
            
            # Extract user ID (sub claim)
            user_id = payload.get('sub')
            return user_id
        
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.DecodeError:
            raise Exception("Invalid token")
        except Exception as e:
            raise Exception(f"Error decoding token: {str(e)}")
