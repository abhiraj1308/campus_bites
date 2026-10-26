@'
# 🍔 Campus Bites - Canteen Pre-Ordering Portal

Campus Bites is a full-stack web application designed to streamline college campus canteen food ordering, reduce queue congestion, and optimize kitchen operations. Built with Python (Flask), SQLite, and Bootstrap 5.

---

## 🚀 Key Features
- **Multi-Cuisine Counter System:** Categorized menu management across Chinese, South Indian, North Indian, Snacks, and Beverages counters.
- **Dynamic UPI Payment Gateway:** Generates instant scannable NPCI-compliant UPI QR codes for digital payments alongside Pay-at-Counter options.
- **Live Kitchen Operations Dashboard:** Real-time vendor interface to filter orders by cuisine counters and update live preparation statuses.
- **Auto-Refreshing Student Receipt:** Zero-JavaScript status page that updates every 5 seconds to show live preparation progress.

---

## 🛠️ Tech Stack
- **Backend:** Python, Flask, Flask-SQLAlchemy, Werkzeug (WSGI)
- **Database:** SQLite (`canteen.db`)
- **Frontend:** HTML5, Bootstrap 5, Jinja2 Templating
- **Integrations:** QR Code Generator API (`api.qrserver.com`)

---

## 💻 Running Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/abhiraj1308/campus_bites.git](https://github.com/abhiraj1308/campus_bites.git)
   cd campus_bites
