This project demonstrates how to build a simple Q&A system using Python, Django, and OpenAI's GPT. The system can answer questions based on the context provided from a specific article. The user interface is built using HTML and Tailwind.

## Getting Started
1. Clone the repository:

```bash
    git clone https://github.com/amirtds/python-openai
```

1. Install the required packages:
    
```bash
    pip install -r requirements.txt
```

1. Create a `.env` file in the root directory of the project and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key
```

1. Run migration and start the server:

```bash
    cd llm_api
    python manage.py migrate
    python manage.py runserver
```

1. Run the frontend:

```bash
    cd frontend
    python -m http.server 8080
```
```
python-openai
├─ .DS_Store
├─ .gitignore
├─ LICENSE
├─ README.md
├─ frontend
│  ├─ .DS_Store
│  └─ index.html
├─ llm_api
│  ├─ .DS_Store
│  ├─ api
│  │  ├─ .DS_Store
│  │  ├─ .streamlit
│  │  │  ├─ config.toml
│  │  │  └─ credentials.toml
│  │  ├─ __init__.py
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ default.sqlite
│  │  ├─ migrations
│  │  │  └─ __init__.py
│  │  ├─ models.py
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  └─ views.py
│  ├─ indexed_documents
│  │  ├─ default__vector_store.json
│  │  ├─ docstore.json
│  │  ├─ graph_store.json
│  │  └─ index_store.json
│  ├─ llm_api
│  │  ├─ __init__.py
│  │  ├─ asgi.py
│  │  ├─ settings.py
│  │  ├─ urls.py
│  │  └─ wsgi.py
│  ├─ manage.py
│  ├─ original_data
│  │  └─ original_documents
│  │     ├─ 国内智能网联汽车的发展现状v5.docx
│  │     └─ 国内智能网联汽车的发展现状v6.docx
│  ├─ postdata
│  │  ├─ __init__.py
│  │  ├─ admin.py
│  │  ├─ apps.py
│  │  ├─ migrations
│  │  │  └─ __init__.py
│  │  ├─ models.py
│  │  ├─ templates
│  │  │  ├─ success.html
│  │  │  └─ upload.html
│  │  ├─ tests.py
│  │  ├─ urls.py
│  │  ├─ utils
│  │  │  ├─ create_index.py
│  │  │  ├─ create_name.py
│  │  │  └─ test.py
│  │  └─ views.py
│  └─ wandb
└─ requirements.txt

```