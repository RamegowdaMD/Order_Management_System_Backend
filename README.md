# Order Management System Backend

Django-based order management system with integrated payment processing and notifications.

## Services

- **Users**: User authentication and management
- **Products**: Product catalog management
- **Orders**: Order processing and tracking
- **Payments**: Stripe payment integration
- **Notifications**: Email notifications via Sendinblue

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Environment Variables

Create `.env` file:
```
SENDINBLUE_API_KEY=your_key
STRIPE_SECRET_KEY=your_key
```
