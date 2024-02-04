
# Mail Assistant CLI

Mail Assistant is an AI powered personalized bot which works on the email inbox threads. This bot provides multiple functionalities including 

- Get your queries resolved using this intelligent Bot.
- Reads your inbox right from your terminal
- Never miss events that are not in calendar but comminucated over email.


## Environment Variables

To run this `mail assistant`, you will need to add the following environment variables to your `.env` file

- `OPENAI_API_KEY`

- `DB_URI`

- `CHROMA_DB_PATH`

For simplicity please copy `.env.example` to `.env`

PostgresSQL is required for running the project. Make sure that username `postgres` with password `karthik` exists.

## Run Locally

Clone the project

```bash
  git clone https://github.com/IITDh-Hackathon/email-chatbot.git
```

Go to the project directory

```bash
  cd email-chatbot
```
Create Virtualenv

```bash
  python3 -m venv myenv
```

Activate `myenv`

```bash
  source myenv/bin/activate

```


Install dependencies

```bash
  pip3 install -r requirements.txt
```

Start Sync Service

The sync service is written to sync gmails to local db. When first run you need to authorize your Gmail Account.

```
  cd services
  python3 sync_service.py
```

Running CLI Application

while the sync service is running. open new terminal to start CLI application.
run



```bash
  cd src/
  python3 main.py
```


Please wait few minutes before starting CLI, as the sync service needs to download many emails initially.





## Demo

[Demo of Mail Assistant](https://www.loom.com/share/624f44cb8aa24e90bdef63225ba5b0e8)


## TechStack
- Python
- LangChains 
- OpenAI LLMs (GPT-3.5 and GPT-4)
- Textual UI (For Terminal UI)
- [Simplegmail](https://github.com/jeremyephron/simplegmail)(Gmail api client)

## Authors

- [@karthikmurakonda](https://github.com/karthikmurakonda)
- [@karthik-k-18](https://github.com/karthik-k-18)
- [@mr-rajashekhar](https://github.com/mr-rajashekhar)
- [@bharathchandra0915](https://github.com/bharathchandra0915)
