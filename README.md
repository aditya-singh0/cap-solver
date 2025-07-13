# Captcha Solver Frontend

This is the frontend for the Captcha Solver SaaS application, hosted on GitHub Pages.

## Features

- Modern, responsive UI built with Tailwind CSS
- User registration and login functionality
- CAPTCHA solving demo interface
- Payment integration with UPI
- Mobile-friendly design

## Deployment

This frontend is automatically deployed to GitHub Pages. The site is available at:
https://aditya-singh0.github.io/cap-solver-frontend/

## Backend

The backend API is hosted on Railway at:
https://your-railway-app-name.railway.app

## Local Development

To run the frontend locally:

```bash
# Serve the static files
python3 -m http.server 8080 --directory .
```

Then visit http://localhost:8080

## API Configuration

Update the `API_BASE_URL` in `index.html` to point to your Railway backend URL. 