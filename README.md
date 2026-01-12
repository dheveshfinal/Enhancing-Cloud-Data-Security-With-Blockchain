# Enhancing Cloud Data Security with Blockchain

## Abstract
The goal of this project is to **secure cloud-stored data** using:

- **Dynamic AES encryption** for unique keys per file  
- **Blockchain-based decentralized key management** for secure, tamper-proof key storage  
- **Elliptic Curve Cryptography (ECC)** for safe file sharing and transmission  

This system improves **confidentiality, integrity, and security** of cloud data while addressing the limitations of traditional centralized storage.

---

## Problem Definition
- Cloud storage is convenient and scalable, but **data is vulnerable** to unauthorized access.  
- Centralized key management creates a **single point of failure**.  
- A **flexible, decentralized solution** is required to protect sensitive data.  
- This project combines **dynamic AES encryption** with **blockchain key management** to provide robust cloud data security.

---

## Literature Survey
1. **Hybrid AES-ECC Model:** Combines AES encryption and ECC-generated keys for secure, efficient cloud storage.  
2. **Blockchain Key Management:** Stores encryption keys in a decentralized, immutable ledger to prevent tampering.  
3. **Dynamic AES Encryption:** Generates unique keys per file and rotates them regularly to reduce the impact of key compromise.

---

## Project Location
Store the project code at:

C:\Users\dheve\OneDrive\Desktop\Code (2)\Code (2)\Code\Code


---

## Running the Django Server
1. Open terminal/CMD in the project folder:
```cmd
cd "C:\Users\dheve\OneDrive\Desktop\Code (2)\Code (2)\Code\Code"

Run the development server:

python manage.py runserver


Open in browser:

http://127.0.0.1:8000/

Smart Contract Setup (Truffle + Ganache)

Navigate to the folder containing truffle-config.js.

Compile contracts:

truffle compile


Deploy contracts to Ganache:

truffle migrate --reset --network development


Copy UserContract address from the deployed contracts and paste in ./myapp/views.py:

user_contract_address = "paste_address_here"


Copy any account address from Ganache and paste in ./myapp/views.py:

one_account = "paste_account_here"

Email Setup (Gmail)

Enable 2-Step Verification: Google 2-Step Verification

Create an App Password: Google App Passwords

Add it to settings.py:

EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

Notes

Do not commit secrets (Firebase keys, passwords) to GitHub. Add them to .gitignore:

*.json
*.env


Ensure Ganache is running before deploying or testing smart contracts.

Use a Python virtual environment:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

Author

Dhevesh Arun


---

If you want, Dhevesh, I can also **add a small diagram section or badges** (Python, Django, Solidity, GitHub stars) so the README looks **super professional** on GitHub.  

Do you want me to do that?
