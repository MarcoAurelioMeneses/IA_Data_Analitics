from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
assistant = client.beta.assistants.create(
  instructions="Você é um analista de dados senior e deve fazer analises sobre os documentos",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}]
)


# Upload a file with an "assistants" purpose
file = client.files.create(
  file=open("dados/uploaded_3d07cbcc-dd09-43e8-bb19-c22767e4f935.csv", "rb"),
  purpose='assistants'
)

# Create an assistant using the file ID
assistant = client.beta.assistants.create(
  instructions="Você é um analista de dados senior e deve fazer analises sobre os documentos",
  model="gpt-4o",
  tools=[{"type": "code_interpreter"}],
  tool_resources={
    "code_interpreter": {
      "file_ids": [file.id]
    }
  }
)

thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "Preciso saber quantas escolas por CREDE estão cadastradas",
      "attachments": [
        {
          "file_id": file.id,
          "tools": [{"type": "code_interpreter"}]
        }
      ]
    }
  ]
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

run_steps = client.beta.threads.runs.steps.list(
  thread_id=thread.id,
  run_id=run.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))
message_content = messages[0].content[0].text

print(message_content)
