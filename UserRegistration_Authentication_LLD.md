
## **📌 Low-Level Design (LLD)**
### **🔹 Components**
1. **Database Tables**
2. **API Endpoints**
3. **Authentication Flow**
4. **Data Validation & Security**
5. **Error Handling**
6. **Libraries & Technologies**


## **2️⃣ API Endpoints**
### **🔹 Register User**
- **Endpoint:** `POST /api/auth/register`
- **Description:** Creates a new user account.
- **Request Body (JSON)**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "securepassword"
}
```
- **Process Flow:**
  1. Validate input data.
  2. Check if the email already exists.
  3. Hash the password using **bcrypt**.
  4. Store user details in the database.
  5. Return success response.

- **Response (Success - 201)**
```json
{
  "message": "User registered successfully."
}
```
- **Response (Error - 400)**
```json
{
  "error": "Email already exists."
}
```

---

### **🔹 Login User**
- **Endpoint:** `POST /api/auth/login`
- **Description:** Authenticates user and returns a JWT token.
- **Request Body (JSON)**
```json
{
  "email": "john.doe@example.com",
  "password": "securepassword"
}
```
- **Process Flow:**
  1. Validate input data.
  2. Fetch user details using the email.
  3. Verify password using **bcrypt**.
  4. Generate **JWT token** with expiration.
  5. Return token and user details.

- **Response (Success - 200)**
```json
{
  "token": "jwt_token_here",
  "user_id": 1
}
```
- **Response (Error - 401)**
```json
{
  "error": "Invalid email or password."
}
```

---

### **🔹 Logout User**
- **Endpoint:** `POST /api/auth/logout`
- **Description:** Invalidates the session (for session-based auth).
- **Process Flow:**
  1. Blacklist or delete the JWT token (if applicable).
  2. End user session (for session-based authentication).
  3. Return logout success message.

- **Response (Success - 200)**
```json
{
  "message": "Logout successful."
}
```

---

## **3️⃣ Authentication Flow**
1. **Registration**
   - User provides email and password.
   - Password is hashed using `bcrypt`.
   - User data is stored securely.
  
2. **Login**
   - User enters email and password.
   - Password is validated.
   - JWT token is generated and returned.

3. **Token Validation (Middleware)**
   - All protected routes check the **Authorization header** for a valid JWT token.
   - The token is verified and decoded to extract user information.

---

## **4️⃣ Data Validation & Security**
- **Input Validation**
  - Use regex for **email format validation**.
  - Enforce **strong password policy** (minimum length, special characters).
  
- **Password Security**
  - Store passwords **hashed using bcrypt** (never store raw passwords).
  - Use a **salt** for added security.

- **JWT Security**
  - Use **strong secret keys** for JWT signing.
  - Set **token expiration** (e.g., `1 hour`).
  - Store JWT securely (HTTP-only cookies or local storage with secure policies).

- **SQL Injection Prevention**
  - Use **parameterized queries** or an **ORM** like Django ORM.

---

## **5️⃣ Error Handling**
### **Common Errors & Handling**
| Scenario | Error Message | HTTP Status Code |
|----------|--------------|------------------|
| Email already registered | `"Email already exists."` | `400 Bad Request` |
| Invalid email or password | `"Invalid email or password."` | `401 Unauthorized` |
| Missing required fields | `"First name is required."` | `400 Bad Request` |
| Token expired/invalid | `"Token expired or invalid."` | `401 Unauthorized` |

---

## **6️⃣ Technologies & Libraries**
| Component            | Suggested Technology |
|----------------------|---------------------|
| Backend Framework    | Django (Django Rest Framework)|
| Database            | PostgreSQL / MySQL  |
| Authentication      | JWT (pyjwt) / OAuth2 |
| Password Hashing    | bcrypt |
| Input Validation    | marshmallow / pydantic |
| Security           | CSRF protection, HTTPS |

---
