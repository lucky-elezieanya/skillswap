## 🌐 SkillSwap

**SkillSwap** is a full-stack platform built with **Django (DRF)** and **Next.js (App Router + TypeScript)** that enables users to **exchange skills and services** through either **barter** or **secure escrow-based transactions**.

It connects professionals, freelancers, and hobbyists within their local or global communities, enabling value-for-value collaborations.

## 🔧 Tech Stack

| Layer    | Technology                                  |
| -------- | ------------------------------------------- |
| Frontend | Next.js (App Router), TypeScript            |
| UI       | TailwindCSS, ShadCN UI, Lucide              |
| Backend  | Django, Django REST Framework               |
| Auth     | Clerk / Custom Auth (with JWT)              |
| Database | MongoDB (via Prisma ORM)                    |
| Storage  | Cloudinary (Image/Video Uploads)            |
| Payments | Stripe (Escrow + Direct Payments)           |
| Realtime | Socket.io (for chat/notifications)          |
| Hosting  | Vercel (Frontend), Railway/Render (Backend) |

## 🧩 Features

- 🔄 **Skill Barter**: Exchange services without money.
- 💵 **Escrow System**: Pay securely and release after service.
- 🎥 **Media Uploads**: Upload videos/images via Cloudinary.
- 💬 **Live Chat**: Real-time messaging between users.
- 🔍 **Advanced Search & Filters**: Search by skill, location, etc.
- 📋 **Profiles**: Showcasing skills, completed jobs, and ratings.
- 📈 **Dashboard**: For users to manage requests, offers, and escrow.
- 🔐 **Secure Auth**: Clerk integration or JWT custom auth system.

## 📁 Project Structure

```plaintext
skillswap/
│
├── backend/ # Django + DRF API
│ ├── core/ # Django apps (accounts, skills, barter, escrow)
│ ├── media/ # Uploaded content
│ ├── manage.py
│ └── requirements.txt
│
├── frontend/ # Next.js 15 (App Router)
│ ├── app/ # Pages & routing
│ ├── components/ # UI Components (ShadCN, Carousel, etc.)
│ ├── lib/ # API helpers & utilities
│ ├── styles/ # Tailwind config
│ └── tsconfig.json
│
├── prisma/ # Prisma schema and migrations
│ ├── schema.prisma
│ └── migrations/
│
├── .env # Environment variables
├── .gitignore
└── README.md

```

---

## 🚀 Getting Started

### 🔑 Prerequisites

- Node.js ≥ 18
- Python ≥ 3.10
- MongoDB
- Cloudinary Account
- Stripe Account
- Clerk Account (or implement JWT)

---

### 1️⃣ Clone the Repo

```bash
git clone https://github.com/yourusername/skillswap.git
cd skillswap
```

---

### 2️⃣ Set Up Environment Variables

Create a `.env` file in both `frontend/` and `backend/` directories.

#### Example `backend/.env`

````env
DEBUG=True
SECRET_KEY=your-django-secret
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/skillswap
CLOUDINARY_API_KEY=your-key
CLOUDINARY_API_SECRET=your-secret
```markdown

#### Example `frontend/.env.local`

```env
NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME=your-cloud
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your-pub-key
NEXT_PUBLIC_API_URL=http://localhost:8000/api
````

---

### 3️⃣ Backend Setup (Django)

```bash
cd backend
python -m venv env
source env/bin/activate  # Use env\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

### 4️⃣ Frontend Setup (Next.js)

```bash
cd frontend
npm install
npm run dev
```

---

## 📡 API Documentation

- API base: `http://localhost:8000/api/`
- All endpoints follow RESTful conventions.
- Auth via Clerk or JWT with `Authorization: Bearer <token>`

---

## 🛠️ Development Notes

- Prisma is used to manage MongoDB with strict type safety.
- Cloudinary handles all media uploads (video + images).
- Stripe handles all escrow and post-service payments.
- Use `react-hook-form` and `zod` for form validation.
- Built with reusable components and utility libraries.

---

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend (e.g. unit tests with Jest/Playwright)
cd frontend
npm run test
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a pull request

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

## 📬 Contact

- **Author**: Lucky Elezieanya
- **Email**: [your.email@example.com](mailto:your.email@example.com)
- **YouTube**: [Guruhub Tech and Fixes](https://www.youtube.com/@guruhubtech)

---

> 💡 _SkillSwap — Powering collaborative value exchange for everyone._

```


```
