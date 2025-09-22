# Odoo Boilerplate Setup

This repository provides a boilerplate setup for running **Odoo** with Docker.  
It supports both **Windows (via WSL + Docker Desktop)** and **Linux (Docker only)**.

---

## 📦 Requirements

- **Windows**:  
  - [WSL](https://learn.microsoft.com/en-us/windows/wsl/install)  
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/)  

- **Linux**:  
  - [Docker](https://docs.docker.com/engine/install/)  

---

## ⚙️ Installation Steps

1. **Clone this repository into your working directory.**
   > ℹ️ The project does **not** need to be inside WSL, it can be placed anywhere.

   ```bash
   git clone <this-repo-url> my-odoo-project
   cd my-odoo-project 
    ```
2. **Clone the Odoo Enterprise Addons into your machine..**
   (This requires Odoo Enterprise)
   ```bash
   git clone <enterprise-repo-url>
   ```
3. **Create a new repository from this boilerplase as a template**
   > Use GitHub's "Start with a Template" option.

4. **Configure environment variables:
   > Copy .env.example -> .env
   ```bash
   cp .env.example .env
   ```
   > Edit .env and updaate
     > ODOO_ENTERPRISE_LOCAL_PATH=[path to the the enterprise addons]
     > Database credentials: DB_USER, DB_PASSWORD, DB_TABLE
5. **Custom Addons projects**
   > Create the addons project folder containing the __manifest__.py and __init__pny
   > Update docker-compose.yml by adding the path of the addons into the command block
   > example:
   ```yaml
   services:
     odoo:
      command: ['odoo', '--addons-path=/var/lib/odoo/enterprise,/var/lib/odoo/tutorials', "-d", "${DB_TABLE}" , "-r", "${DB_USER}", "-w", "${DB_PASSWORD}", "-i", "base,web", "--dev", "xml"]
      volumes:
        - ./${ODOO_ENTERPRISE_LOCAL_PATH}:/var/lib/odoo/enterprise
        - ./addons:/var/lib/odoo/addons:rw
        - ./extra-addons:/mnt/extra-addons:rw
        - ./config:/etc/odoo:rw
        - ./odoo-logs:/etc/odoo-logs:rw
        - ./tutorials:/var/lib/odoo/tutorials:rw
   ```

6. **Run docker container**
  ```bash
  docker-compose up --build -d
  ```

  7. **Visit the site on http://localhost:8069**
