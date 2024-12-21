# **Book Store API**
  This project is a feature-rich API for managing a virtual book store with three types of users: Admin, Buyer, and Seller. The API includes functionalities for user registration, login, shop creation, book management, and secure payment processing using Stripe. Below is a breakdown of the user roles and their capabilities.

## **User Roles and Functionalities**

### **1. Admin**

  The admin has a comprehensive view of all users registered on the platform.
  Admin privileges are limited to user management.

### **2. Buyer**

  Buyers are the primary customers of the book store. They have the following capabilities:

**View Shops and Books:**

  A buyer can browse all available shops.
  They can view the list of books in any selected shop.

**Purchase Books:**

  Buyers can choose a book by its ID and add it to their purchase record, linked with their user ID.

**Stripe Payment Integration:**

  Stripe is used for secure payment processing.
  Webhooks, such as payment_intent.successful, are integrated for handling payment confirmation events.
  Buyers who have already purchased a book won't see the checkout page again when re-calling the payment API.

**🛑 Note: Only buyers are authorized to make payments.**

### **3. Seller**

  Sellers are responsible for managing shops and books. They can:

**Add and Manage Shops:**

  Sellers can create multiple shops and manage their information.

**Add and Manage Books:**

  Sellers can add books to their shops and update them as needed.
  
**View Own Shops:**

  Sellers have access to all their shops and the associated information.

### **Authentication**
  This API uses JWT Authentication to ensure secure access.

**Registered Users Only:**

  Users must register and log in to gain access to the API.
  Without authentication, users are restricted from using any endpoints.

### **Technologies Used**
  **Payment Integration:** Stripe for handling payments and webhooks.
  **Authentication:** JSON Web Tokens (JWT) for secure access.

**How to Use**

Register as a user.
Log in using your credentials to obtain a JWT token.
Use the token for authorized access to API features.
Feel free to further enhance this based on specific implementation details. Let me know if you'd like more customization!






You said:
good but if i add this, it won't show the highlighted text or any other things
ChatGPT said:
ChatGPT
You're correct. GitHub README files are written in Markdown, so you'll need to format the text with Markdown syntax for proper styling. Here's the adjusted version of the README using Markdown:

Book Store API
This project is a feature-rich API for managing a virtual book store with three types of users: Admin, Buyer, and Seller. The API includes functionalities for user registration, login, shop creation, book management, and secure payment processing using Stripe. Below is a breakdown of the user roles and their capabilities.

User Roles and Functionalities
1. Admin
The admin has a comprehensive view of all users registered on the platform.
Admin privileges are limited to user management.
2. Buyer
Buyers are the primary customers of the book store. They have the following capabilities:

View Shops and Books:
A buyer can browse all available shops.
They can view the list of books in any selected shop.
Purchase Books:
Buyers can choose a book by its ID and add it to their purchase record, linked with their user ID.
Stripe Payment Integration:
Stripe is used for secure payment processing.
Webhooks, such as payment_intent.successful, are integrated for handling payment confirmation events.
Buyers who have already purchased a book won't see the checkout page again when re-calling the payment API.
🛑 Note: Only buyers are authorized to make payments.

3. Seller
Sellers are responsible for managing shops and books. They can:

Add and Manage Shops:

Sellers can create multiple shops and manage their information.
Add and Manage Books:

Sellers can add books to their shops and update them as needed.
View Own Shops:

Sellers have access to all their shops and the associated information.
Authentication
This API uses JWT Authentication to ensure secure access.

Registered Users Only:
Users must register and log in to gain access to the API.
Without authentication, users are restricted from using any endpoints.
Technologies Used
Payment Integration: Stripe for handling payments and webhooks.
Authentication: JSON Web Tokens (JWT) for secure access.
How to Use
Register as a user.
Log in using your credentials to obtain a JWT token.
Use the token for authorized access to API features.
