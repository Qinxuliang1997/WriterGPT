This project demonstrates how to build a simple Q&A system using Python, Django, and OpenAI's GPT. The system can answer questions based on the context provided from a specific article. The user interface is built using HTML and Tailwind.

## Getting Started
1. Clone the repository:

```bash
    git clone https://github.com/Qinxuliang1997/WriterGPT
```

2. Install the required packages:
    
```bash
    pip install -r requirements.txt
```

```bash
    cd frontend/user_input_form
    npm install
```

3. [Set your OPENAI_API_KEY Environment Variable](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)

4. Run migration and start the server:

```bash
    cd llm_api
    python manage.py migrate
    python manage.py runserver
```

5. Run the frontend:

```bash
    cd frontend/user_input_form
    npm start
```