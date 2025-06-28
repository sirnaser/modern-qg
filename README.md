
# Modern Question Generator

**Backend**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
uvicorn backend.main:app --reload   # Server starts on http://127.0.0.1:8000
```

**Front‑end**

There is no build step – the static HTML (with Tailwind CDN) is served automatically by FastAPI at the root URL.  
Open http://127.0.0.1:8000 in your browser.

**Workflow**

1. در تب «از محتوا» یک فایل Markdown را بارگذاری کنید تا پرسش‌های جدید تولید شود.  
2. در تب «از نمونه سؤالات» یک فایل LaTeX نمونه را آپلود کنید تا پرسش‌های مشابه ایجاد شود.  
3. بعد از اتمام پردازش، یک لینک برای دانلود خروجی `.tex` نمایش داده می‌شود.

> **نکته**: برای رندر کردن فایل در مرورگر، می‌توانید از افزونه‌هایی مثل *MathJax* یا سرویس‌های آنلاین که LaTeX را پیش‌نمایش می‌کنند استفاده کنید، اما داخل پروژه به‌صورت پیش‌فرض فقط امکان دانلود وجود دارد.
