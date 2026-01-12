Enhancing Cloud Data Security with Blockchain
Abstract

The goal of this project is to secure cloud-stored data using dynamic AES encryption, blockchain-based decentralized key management, and Elliptic Curve Cryptography (ECC). Each file gets a unique, constantly changing AES key, while blockchain ensures secure storage of these keys in a tamper-proof way. ECC adds extra security for file sharing and transmission. This system improves data confidentiality, integrity, and security in modern cloud environments.

Problem Definition

Cloud storage is convenient and scalable, but data is vulnerable to unauthorized access.

Centralized key management creates a single point of failure.

A more flexible and decentralized solution is needed to protect sensitive data.

This project uses blockchain and dynamic AES to solve these issues, making cloud storage safer and more reliable.

Literature Survey (Short)

Hybrid AES-ECC Model: Combines AES encryption and ECC keys for secure, fast cloud storage.

Blockchain Key Management: Decentralized ledger for tamper-proof key storage.

Dynamic AES: Unique keys per file, rotated regularly to prevent key compromise.

Project Location

Store the code at:

C:\Users\dheve\OneDrive\Desktop\Code (2)\Code (2)\Code\Code

Running the Django Server

Open CMD in project folder:

cd "C:\Users\dheve\OneDrive\Desktop\Code (2)\Code (2)\Code\Code"


Run:

python manage.py runserver


Open in browser:

http://127.0.0.1:8000/

Smart Contract Setup (Truffle + Ganache)

Open terminal in folder with truffle-config.js.

Compile contracts:

truffle compile


Deploy contracts to Ganache:

truffle migrate --reset --network development


Copy UserContract address from deployed contracts and paste in ./myapp/views.py:

user_contract_address = "paste_address_here"


Copy any account address from Ganache accounts and paste in ./myapp/views.py:

one_account = "paste_account_here"

Email Setup (Gmail)

Enable 2-Step Verification: Google 2-Step Verification

Create an App Password: Google App Passwords

Add it to settings.py:

EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'

Notes

Never commit secrets like Firebase keys or passwords. Add them to .gitignore:

*.json
*.env


Make sure Ganache is running before deploying or testing contracts.

Use virtual environment for Python dependencies:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
