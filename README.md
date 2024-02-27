This project is a simple writter system using Python, Django, LlamaIndex, and OpenAI's GPT. The system can write content based on the context provided from some related uploaded articles. The user interface is built using Node.js and React.

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

windows: 
```
setx OPENAI_API_KEY “<yourkey>”
```

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

6. Addition

make new path: WriterGPT\llm_api\original_data\original_documents