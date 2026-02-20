# Custom E‑Commerce Shop (WhatsApp checkout)
This repository is a full, self-contained Django project scaffold implementing the e‑commerce requirements you asked for:

- Fully **owned** codebase (no third-party platforms required).
- Dark-mode responsive UI, mobile-first, cards for categories & products.
- Admin panel to manage categories, products, images, and orders.
- Session-based cart (no login required for customers).
- Checkout saves order in DB and redirects customer to WhatsApp (`wa.me`) with a prefilled order message.
- Easy to extend later (add payment gateway, shipping, multi-user, analytics).

## Quick start (development)
1. Create virtualenv and install requirements:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Run migrations and create admin user:
```bash
python manage.py migrate
python manage.py createsuperuser
```
3. Start the dev server:
```bash
python manage.py runserver
```
4. Open `http://127.0.0.1:8000/` — site home.
5. Admin panel: `http://127.0.0.1:8000/admin/` to manage categories/products/orders/settings.

## Deployment (Docker)
A `Dockerfile` and `docker-compose.yml` are included. Configure environment variables in `.env` file (example provided).

## Project Structure (high level)
- `project/` – Django project settings & URLs
- `store/` – primary app (models, views, templates)
- `static/` – CSS & JS
- `templates/` – main templates (base, home, product pages, cart, checkout)


Notes:
- By default the project uses SQLite for simplicity. You can switch to PostgreSQL by editing `project/settings.py` and `.env`.
- Images are stored in `media/` by default. For production, use an S3-compatible storage or attach a volume.

If you want, I can also:
- Add a sample dataset (categories & products) fixture file.
- Provide automated deploy scripts for Hetzner/OVH/DigitalOcean.
