# 🌿 AQI Tracker and Exposure Monitoring System

## 📌 Project Overview
AQI Tracker and Exposure Monitoring System is a web-based project that helps users monitor Air Quality Index (AQI), temperature, rain, and UV index for different cities.

The system also provides health advisory, exposure monitoring, notification alerts, and secure login/signup functionality.

---

## 🚀 Main Features
- User Signup and Login  
- Strong password validation  
- AQI Dashboard  
- City search functionality  
- AQI, Temperature, Rain, UV display  
- 24-hour graphs using Chart.js  
- Health Advisory page  
- Exposure Monitoring page  
- Notification alerts  
- Logout functionality  
- Admin access  
- Exposure page opens only after login  

---

## 🔐 Login and Signup Validation
Password must contain:
- Minimum 8 characters  
- One uppercase letter  
- One lowercase letter  
- One number  
- One special character  

Email format is also validated.

---

## 🛠️ Technologies Used

### Programming Languages
- Python  
- HTML  
- CSS  
- JavaScript  
- SQL  

### Frameworks & Libraries
- Flask  
- Chart.js  
- oracledb  

### Database
- Oracle Database  

### Tools
- VS Code  
- Oracle SQL Developer  

---

## 🗂️ Project Structure
AQI_Project/
│
├── app.py
├── templates/
│ ├── dashboard.html
│ ├── login.html
│ ├── signup.html
│ ├── exposure.html
│ ├── healthadvisory.html
│ ├── about.html
│ ├── admin.html
│
├── static/
│ ├── style.css
│ ├── script.js


---

## 🗄️ Database Tables
- USERS  
- CITIES  
- AQI_DATA  
- FORECAST  
- EXPOSURE  
- NOTIFICATION  

---

## ⚙️ How the Project Works
1. User opens website  
2. User signs up or logs in  
3. Dashboard opens  
4. User searches city  
5. Data fetched from Oracle DB  
6. AQI, temp, rain, UV displayed  
7. Graphs shown using Chart.js  
8. Notification gives advice  
9. Exposure page shows history  
10. Only logged-in user can access exposure  
11. Logout ends session  

---

## ▶️ How to Run Project

### Step 1: Clone
git clone https://github.com/jyoti2225/AQI-Tracker-Exposure-System.git


### Step 2: Install packages
pip install flask
pip install oracledb


### Step 3: Setup Database
Create tables:
- USERS  
- CITIES  
- AQI_DATA  
- FORECAST  
- EXPOSURE  
- NOTIFICATION  

---

### Step 4: Configure DB
python
def get_connection():
    return oracledb.connect(
        user="your_username",
        password="your_password",
        dsn="localhost:1521/XEPDB1"
    )

Step 5: Run
python app.py
Step 6: Open
http://localhost:5000
🔮 Future Scope
Real-time API
Mobile app
More cities
Email alerts
![image alt](https://github.com/jyoti2225/AQI-Tracker-Exposure-System/blob/296392999bcbf52eb0aa0acae50fe57f472d49a7/Screenshot%202026-04-19%20185640.png)

Author
Jyoti
