# Bank Account Transaction Management System

A full-featured Bank Account Transaction Management System built with **Django** and **Bootstrap 5**. This system allows authenticated users to manage their bank accounts, deposit/withdraw money, track real-time balance, search/filter transaction history, and view dynamic dashboard analytics.

---

## 🌟 Features

### 🔑 Part 1: User Authentication
* **User Registration & Login:** New users can sign up and securely log in.
* **Logout & Security:** Only authenticated users can access the dashboard and perform transactions.
* **Data Privacy:** Users can only view their own account details and transaction logs.

### 💳 Part 2: Bank Account Management
* **Account Auto-Creation:** Unique bank account and balance initialization.
* **Dashboard Display:** Shows Account Holder Name, Account Number, and Current Balance.

### 💵 Part 3 & 4: Deposits & Withdrawals
* **Deposit System:** Accepts deposits greater than $0, updates balance instantly, and logs history with success messages.
* **Withdrawal System:** Prevents overdraft (cannot withdraw more than current balance), updates balance, and logs history.

### 📜 Part 5 & 6: Transaction History, Search & Filter
* **Detailed Logs:** Tracks Type (Deposit/Withdrawal), Amount, Timestamp, and Balance After Transaction (newest first).
* **Filter Options:** Filter history by Transaction Type (Deposit/Withdrawal) and Date / Date Range (Start Date to End Date).

### 📊 Part 7: Dashboard Summary
* Overview cards showing **Current Balance**, **Total Deposits**, **Total Withdrawals**, and **Total Transactions**.

### 🎁 Bonus Features Included
* **Bootstrap 5 UI:** Modern, clean, and responsive design.
* **Pagination:** Smooth page navigation for transaction history records.

---

## 📸 Screenshots & UI Previews

All required UI screenshots (Registration, Login, Dashboard, Deposit, Withdraw, Transaction History) have been uploaded to Google Drive.

* **Google Drive Link for Screenshots:** [Insert Your Google Drive Link Here]

---

## 🛠️ Tech Stack
* **Framework:** Python / Django
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Database:** SQLite (Default Django DB)

---

## 🚀 Setup & Installation Instructions

Follow these step-by-step instructions to set up and run the project locally on your machine:

### Step 1: Clone the Repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd bank_project

python -m venv venv
source venv/Scripts/activate

python3 -m venv venv
source venv/bin/activate

pip install django

python manage.py makemigrations
python manage.py migrate