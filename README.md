# Flask Notes Webapp — Docker Compose

A minimal note-taking web application built with Flask and MySQL, containerized using Docker and orchestrated with Docker Compose. This project provides both a simple web UI and a REST API for creating and listing notes, with persistent MySQL storage.

**🔗 GitHub Repository:** https://github.com/davidahdy/flask-notes-compose

---

## 🚀 Features

- **Flask-based web app** with HTML UI and REST API endpoints
- **MySQL database** with persistent storage using Docker volumes
- **Environment variables** for secure configuration management
- **Docker Compose** for multi-container orchestration
- **Health checks** for both web and database services
- **Non-root container security** implementation
- **AWS EC2 deployment ready**

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Flask** | Python microframework for web development |
| **MySQL 8.x** | Relational database for data persistence |
| **Docker** | Containerization platform |
| **Docker Compose** | Multi-container orchestration |
| **Gunicorn** | WSGI HTTP server for production |

---

## 📋 Prerequisites

Before running this project, ensure you have:

- **Docker** (version 20.10+) and **Docker Compose** (v2) installed
- **Git** for cloning the repository
- **Basic terminal/command line knowledge**
- **AWS EC2 instance** (for cloud deployment) or local machine

### Installation Links:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## 📁 Project Structure

```
flask-notes-compose/
├── .env                    # Environment variables (DO NOT COMMIT)
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore rules
├── Dockerfile             # Web app container build file
├── README.md              # This documentation
├── app/                   # Flask application source code
│   ├── __init__.py        # Flask app initialization
│   ├── static/            # Static assets (CSS, JS, images)
│   └── templates/         # HTML templates
│       └── index.html     # Main UI template
├── db/                    # Database configuration
│   └── init/              # SQL initialization scripts
│       └── 001_create_table.sql
├── docker-compose.yml     # Docker Compose configuration
├── docs/                  # Documentation files
└── requirements.txt       # Python dependencies
```

---

## ⚙️ Environment Variables

The application uses the following environment variables (defined in `.env`):

| Variable | Description | Example |
|----------|-------------|---------|
| `MYSQL_ROOT_PASSWORD` | MySQL root user password | `secure_root_pass123` |
| `MYSQL_DATABASE` | Database name | `notesdb` |
| `MYSQL_USER` | MySQL application user | `notesuser` |
| `MYSQL_PASSWORD` | MySQL application user password | `user_pass123` |
| `HOST_PORT` | Host port for web application | `8080` |
| `DB_USER` | Database user for Flask app | `notesuser` |
| `DB_PASSWORD` | Database password for Flask app | `user_pass123` |
| `DB_NAME` | Database name for Flask app | `notesdb` |
| `DB_HOST` | Database hostname (container name) | `db` |
| `DB_PORT` | Database port | `3306` |

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/davidahdy/flask-notes-compose.git
cd flask-notes-compose
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
# Edit .env with your preferred MySQL credentials and HOST_PORT
```

### 3. Build and Start the Application

```bash
docker compose up -d --build
```

### 4. Verify Installation

```bash
# Check container status
docker compose ps

# View logs
docker compose logs -f web

# Test health endpoint
curl -i http://localhost:${HOST_PORT:-8080}/healthz
```

**Expected health check response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-08-13T10:30:45Z"
}
```

---

## 🌐 Usage

### Web Interface

Access the web UI at:
- **Local:** http://localhost:8080
- **EC2:** http://\<EC2_PUBLIC_IP\>:8080

![Web Interface](docs/webapp-screenshot.png)

### API Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/notes` | List all notes | N/A |
| `POST` | `/notes` | Create a new note | `{"content":"Your note text"}` |
| `GET` | `/healthz` | Health check | N/A |

### API Examples

#### Create a Note
```bash
curl -X POST http://localhost:8080/notes \
  -H "Content-Type: application/json" \
  -d '{"content":"Buy groceries for the week"}'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "content": "Buy groceries for the week",
  "created_at": "2025-08-13T10:30:45Z",
  "message": "Note created successfully"
}
```

#### List All Notes
```bash
curl http://localhost:8080/notes
```

**Response (200 OK):**
```json
{
  "notes": [
    {
      "id": 1,
      "content": "Buy groceries for the week",
      "created_at": "2025-08-13T10:30:45Z"
    },
    {
      "id": 2,
      "content": "Schedule dentist appointment",
      "created_at": "2025-08-13T09:15:30Z"
    }
  ],
  "total": 2
}
```

#### Health Check
```bash
curl http://localhost:8080/healthz
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-08-13T10:30:45Z"
}
```

---

## 💾 Data Persistence

MySQL data is stored in a Docker named volume (`db-data`) ensuring persistence between container restarts.

### Reset Database
To completely wipe all data:
```bash
docker compose down -v  # Remove containers and volumes
docker compose up -d    # Restart with fresh database
```

### Backup Data
```bash
# Create backup
docker compose exec db mysqldump -u root -p notesdb > backup.sql

# Restore backup
docker compose exec -T db mysql -u root -p notesdb < backup.sql
```

---

## 🔧 Management Commands

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f db
```

### Stop Services
```bash
# Stop containers (keep data)
docker compose down

# Stop containers and remove volumes (lose data)
docker compose down -v
```

### Restart Services
```bash
docker compose restart
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|--------|----------|
| **Access denied for user** | Incorrect MySQL credentials | Verify `.env` credentials match `MYSQL_USER`/`MYSQL_PASSWORD` |
| **Port already in use** | Another service using the port | Change `HOST_PORT` in `.env` to an available port |
| **Health check failing** | Database not ready or connection issues | Check logs: `docker compose logs db web` |
| **Database schema missing** | Initialization scripts not executed | Reset containers: `docker compose down -v && docker compose up -d` |
| **Container won't start** | Resource constraints or Docker issues | Check Docker Desktop resources and restart Docker |

### Debug Commands

```bash
# Check container resource usage
docker stats

# Inspect container details
docker compose exec web ps aux
docker compose exec db ps aux

# Test database connectivity
docker compose exec db mysql -u root -p -e "SHOW DATABASES;"

# Check application logs inside container
docker compose exec web tail -f /var/log/flask-app.log
```

### Security Group (AWS EC2)

Ensure your EC2 Security Group allows:
- **Inbound:** Port 8080 (or your `HOST_PORT`) from `0.0.0.0/0`
- **Outbound:** All traffic

---

## ☁️ AWS EC2 Deployment

### Quick Deployment Steps

1. **Launch EC2 Instance**
   - Use Amazon Linux 2 or Ubuntu 20.04+
   - Install Docker and Docker Compose
   - Configure Security Group for port 8080

2. **Deploy Application**
   ```bash
   # On EC2 instance
   git clone https://github.com/davidahdy/flask-notes-compose.git
   cd flask-notes-compose
   cp .env.example .env
   # Edit .env with production credentials
   docker compose up -d --build
   ```

3. **Access Application**
   - Web UI: `http://<EC2_PUBLIC_IP>:8080`
   - API: `http://<EC2_PUBLIC_IP>:8080/notes`

### Production Considerations

- Use strong, unique passwords in production `.env`
- Set up SSL/TLS termination with a reverse proxy (nginx)
- Implement log rotation and monitoring
- Regular database backups
- Consider using AWS RDS for database in production

---

## 🔐 Security Notes

- **Never commit `.env` files** to version control
- **Use strong passwords** for all database credentials
- **Restrict database access** to trusted networks only
- **Run containers as non-root user** (implemented in Dockerfile)
- **Keep Docker images updated** regularly
- **Monitor application logs** for suspicious activity

---

## 🧪 Testing

### Manual Testing Checklist

- [ ] Web UI loads successfully
- [ ] Can create notes via web form
- [ ] Notes persist after container restart
- [ ] API endpoints return correct responses
- [ ] Health check reports healthy status
- [ ] Database connection works properly

### Automated Testing

```bash
# Run basic API tests
./scripts/test-api.sh  # (if you create this script)
```

---

## 📖 Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Web Browser   │    │   API Client     │
│   (Port 8080)   │    │   (curl/Postman) │
└─────────┬───────┘    └─────────┬────────┘
          │                      │
          └──────────┬───────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Flask Web App  │
            │   (Container)   │
            │   Port 5000     │
            └─────────┬───────┘
                      │
                      ▼
            ┌─────────────────┐
            │ MySQL Database  │
            │   (Container)   │
            │   Port 3306     │
            └─────────────────┘
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---
