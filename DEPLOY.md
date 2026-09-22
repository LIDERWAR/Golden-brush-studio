# Руководство по развертыванию (Deploy) GB STUDIO на VPS сервер

Данное руководство описывает полный цикл развертывания проекта **Popykin Architectural Atelier & Art Studio (GB STUDIO)** на чистом VPS-сервере (Ubuntu 22.04 / 24.04 LTS или Debian 11/12).

---

## 1. Системные требования

- **Сервер:** Любой надежный VPS (Reg.ru, Timeweb, Selectel, Hetzner, Beget и др.).
- **Конфигурация:** Минимум 1 vCPU, 1–2 GB RAM (при 1 GB рекомендуется включить 2 GB Swap), 15+ GB SSD.
- **ОС:** Ubuntu 22.04 LTS или 24.04 LTS (рекомендуется).
- **Домен:** Привязанная A-запись домена (например, `gb-studio.art` и `www.gb-studio.art`), направленная на IP-адрес вашего VPS.

---

## 2. Подготовка сервера (VPS)

Подключитесь к вашему серверу по SSH:
```bash
ssh root@<IP_ВАШЕГО_СЕРВЕРА>
```

### 2.1. Обновление системы и базовые утилиты
```bash
apt update && apt upgrade -y
apt install -y curl git ufw openssl
```

### 2.2. Настройка файрвола (UFW)
Обязательно откройте SSH перед включением файрвола, чтобы не потерять доступ:
```bash
ufw allow OpenSSH
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

### 2.3. Установка Docker и Docker Compose
Установите официальный Docker с помощью официального скрипта:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
rm get-docker.sh
```
Проверьте установку:
```bash
docker --version
docker compose version
```

---

## 3. Размещение и настройка проекта

### 3.1. Клонирование репозитория
Рекомендуется размещать проект в `/opt/gb-studio`:
```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ> /opt/gb-studio
cd /opt/gb-studio
```

### 3.2. Создание файла конфигурации `.env`
Скопируйте шаблон окружения:
```bash
cp .env.example .env
nano .env
```

Отредактируйте параметры:
1. `SECRET_KEY` — сгенерируйте случайный ключ (или запустите `openssl rand -hex 32`).
2. `ALLOWED_HOSTS` — укажите ваш домен и IP сервера:
   ```env
   ALLOWED_HOSTS=gb-studio.art,www.gb-studio.art,<IP_СЕРВЕРА>,localhost
   ```
3. `CSRF_TRUSTED_ORIGINS` — укажите HTTPS адрес вашего домена:
   ```env
   CSRF_TRUSTED_ORIGINS=https://gb-studio.art,https://www.gb-studio.art
   ```
4. `POSTGRES_PASSWORD` — придумайте надежный пароль для базы данных.
5. `DOMAIN_NAME` — ваш основной домен (например, `gb-studio.art`).
6. `CERTBOT_EMAIL` — ваш email для уведомлений Certbot.
7. `AUTO_SEED_DB=true` — автоматически создаст суперпользователя и демо-проекты при первом старте.

Сохраните файл (`Ctrl + O`, затем `Enter`, для выхода `Ctrl + X`).

---

## 4. Запуск и получение SSL сертификата

Сделайте скрипты исполняемыми:
```bash
chmod +x entrypoint.sh init-ssl.sh deploy.sh
```

### Вариант А: Быстрый запуск с автоматическим SSL (Если домен уже привязан)

Если DNS A-записи домена уже смотрят на IP сервера, запустите:
```bash
./init-ssl.sh
```
Этот скрипт:
1. Создаст временный сертификат для первичного старта Nginx.
2. Запустит стек Nginx + Gunicorn + PostgreSQL.
3. Запросит официальный бесплатный SSL-сертификат Let's Encrypt.
4. Автоматически переключит Nginx на защищенный HTTPS режим.

После успешного выполнения скрипта запустите инициализацию базы:
```bash
docker compose up -d
```

---

### Вариант Б: Запуск через скрипт `deploy.sh`
```bash
./deploy.sh
```
Скрипт автоматически проверит `.env`, сгенерирует временный сертификат, соберет образы, запустит миграции, соберет статику и наполнит БД.

После этого, когда DNS-записи вступят в силу, достаточно выпустить постоянный SSL:
```bash
./init-ssl.sh
```

---

## 5. Доступ в Панель Управления (Админку)

- **Адрес админки:** `https://<ВАШ_ДОМЕН>/admin/`
- **Логин по умолчанию:** `admin`
- **Пароль по умолчанию:** `admin2026`

> [!IMPORTANT]
> **Обязательно смените пароль администратора после первого входа!**  
> Сделать это можно в самой панели управления или через терминал:
> ```bash
> docker compose exec web python manage.py changepassword admin
> ```

---

## 6. Регулярное обслуживание и полезные команды

### Просмотр логов в реальном времени
```bash
# Логи Django / Gunicorn
docker compose logs -f web

# Логи Nginx
docker compose logs -f nginx

# Все сервисы
docker compose logs -f
```

### Обновление сайта после изменений в коде
```bash
./deploy.sh
```
Или вручную:
```bash
git pull
docker compose build web
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

### Резервное копирование базы данных PostgreSQL
Создать бэкап:
```bash
docker compose exec -T db pg_dump -U popikin_user popikin_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

Восстановить базу из бэкапа:
```bash
cat backup_YYYYMMDD_HHMMSS.sql | docker compose exec -T db psql -U popikin_user popikin_db
```

### Автоматическое продление SSL
Контейнер `certbot` в `docker-compose.yml` уже настроен на фоновую проверку и обновление сертификатов каждые 12 часов. Никаких дополнительных cron-задач на сервере настраивать не требуется.
