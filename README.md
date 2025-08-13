Alright — I’ll merge both into one **final, polished README** that has:

* A clear introduction & project description
* Technologies used
* Full directory tree
* Setup & run instructions from your old file
* API documentation with examples
* Troubleshooting from your old file
* Deployment notes for EC2
* Security notes

Here’s your final README:

---

```markdown
# 📝 Flask Notes Webapp — Docker Compose (Flask + MySQL)

## 📌 Overview
This is a minimal note-taking web application built with **Flask** and **MySQL**, containerized using **Docker** and orchestrated with **Docker Compose**.  
It provides both a simple web UI and a REST API for creating and listing notes, with persistent MySQL storage.

This project was deployed and tested on **AWS EC2**.

---

## 🛠️ Technologies Used
- **Flask** — Python web framework
- **MySQL** — Relational database
- **Docker** — Containerization
- **Docker Compose** — Multi-container orchestration
- **AWS EC2** — Cloud hosting
- **Linux** — Server OS

---

## 📂 Project Structure
```

flask-notes-compose/
├── .env                  # Environment variables (DO NOT COMMIT)
├── .env.example          # Template for environment variables
├── .gitignore            # Git ignore rules
├── Dockerfile            # Web app container build file
├── README.md             # Project documentation
├── app                   # Flask application source code
│   ├── **init**.py
│   ├── static            # Static assets (CSS, JS, images)
│   └── templates         # HTML templates
│       └── index.html
├── db
│   └── init              # SQL initialization scripts
│       └── 001\_create\_table.sql
├── docker-compose.yml    # Docker Compose configuration
├── docs                  # Documentation files (if any)
└── requirements.txt      # Python dependencies

````

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd flask-notes-compose
````

### 2️⃣ Copy environment variables

```bash
cp .env.example .env
# Edit .env with your MySQL credentials and desired HOST_PORT
```

### 3️⃣ Build & start the services

```bash
docker compose up -d --build
```

### 4️⃣ Check service status

```bash
docker compose ps
docker compose logs -f web
```

### 5️⃣ Test health endpoint

```bash
curl -i http://localhost:${HOST_PORT:-8080}/healthz
```

---

## 🌐 Accessing the App

* **Web UI:** `http://localhost:8080` (or `http://<EC2_PUBLIC_IP>:8080`)
* **API Endpoints:**

| Method | Endpoint   | Description       | Example                                                                                                    |
| ------ | ---------- | ----------------- | ---------------------------------------------------------------------------------------------------------- |
| GET    | `/notes`   | List all notes    | `curl http://localhost:8080/notes`                                                                         |
| POST   | `/notes`   | Create a new note | `curl -X POST http://localhost:8080/notes -H "Content-Type: application/json" -d '{"content":"Buy milk"}'` |
| GET    | `/healthz` | Health check      | `curl http://localhost:8080/healthz`                                                                       |

---

## 📦 Persistent Storage

MySQL data is stored in a **named volume** (`db-data`).
To completely reset the database:

```bash
docker compose down -v
```

---

## 🔄 Stopping / Restarting

```bash
docker compose down
docker compose up -d
```

---

## 🛠 Troubleshooting

* **Access denied for user**
  → Ensure `.env` MySQL credentials match the ones in your app config.

* **Port already in use**
  → Change `HOST_PORT` in `.env`.

* **Health check failing**
  → Run:

  ```bash
  docker compose logs db
  docker compose logs web
  ```

  and ensure your EC2 security group allows inbound traffic on port `8080`.

* **Database schema missing**
  → On first start, tables are created from `db/init/*.sql`.
  To re-run initialization:

  ```bash
  docker compose down -v
  docker compose up -d
  ```

---

## ☁️ Deployment to AWS EC2

1. Launch an EC2 instance (Amazon Linux 2 or Ubuntu) with Docker installed.
2. Clone this repository.
3. Follow the same steps as **"How to Run Locally"**, replacing `localhost` with your EC2 public IP.
4. Make sure your EC2 **Security Group** allows inbound traffic on port `8080`.

---

## 🔒 Security Notes

* Never commit `.env` to version control.
* Use strong passwords for MySQL and API authentication (if added in future).
* Restrict database access to trusted networks.

---
