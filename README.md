# 🍔 Food Ordering API

A RESTful backend for a food ordering system, built with **FastAPI** and **MongoDB**. It supports user authentication, menu management, and order processing with role-based access control (admin vs. regular user).

## ✨ Features

- **Authentication** — user registration & login with JWT-based auth, passwords hashed with `bcrypt`
- **Role-based access control** — separate permissions for `admin` and `user` roles
- **Menu management** — full CRUD on menu items (admin-only for create/update/delete)
- **Order processing** — place orders, calculate totals from live menu prices, track order status (`pending → preparing → ready → delivered → completed / cancelled`)
- **Auto-incrementing integer IDs** — implemented via a dedicated MongoDB `counters` collection instead of default ObjectIds

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Database | MongoDB |
| ODM | [Beanie](https://beanie-odm.dev/) (async, built on Pydantic) |
| Driver | [Motor](https://motor.readthedocs.io/) (async MongoDB driver) |
| Auth | JWT (`python-jose`) + `bcrypt` password hashing |
| Validation | Pydantic schemas |

## 📁 Project Structure

```
.
├── main.py              # FastAPI app entrypoint, router registration
├── database.py          # MongoDB connection & Beanie initialization
├── models/               # Beanie Document models (User, MenuItem, Order)
├── routers/               # API route handlers (auth, menu, orders)
├── schemas/               # Pydantic request/response schemas
└── utils/
    ├── jwt.py             # Token creation & decoding
    ├── id_generator.py    # Auto-increment ID logic via counters collection
    └── clear_db.py        # Utility script to reset the database
```

## 🔌 API Overview

### Auth (`/auth`)
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Log in and receive a JWT |
| GET | `/auth/users` | List all users |

### Menu (`/menu`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/menu/` | List all menu items | Public |
| GET | `/menu/{id}` | Get a single menu item | Public |
| POST | `/menu/` | Create a menu item | Admin only |
| PUT | `/menu/{id}` | Update a menu item | Admin only |
| DELETE | `/menu/{id}` | Delete a menu item | Admin only |

### Orders (`/orders`)
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/orders/` | Place a new order | Authenticated user |
| GET | `/orders/my` | Get the current user's orders | Authenticated user |
| GET | `/orders/` | Get all orders | Admin only |
| PATCH | `/orders/{id}/status` | Update an order's status | Admin only |

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A running MongoDB instance (local or Atlas)

### Installation

```bash
git clone https://github.com/Sejoo-mp/ordering-food-Back-end.git
cd ordering-food-Back-end
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## 📌 Notes

This project was built as a hands-on learning project to practice async Python, FastAPI application structure, and working with MongoDB through an ODM.
