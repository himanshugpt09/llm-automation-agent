from fastapi import FastAPI, HTTPException, Query
import openai
import os
import requests



# Load OpenAI API token from environment variables
OPENAI_TOKEN = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI0ZjEwMDIzMDJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.qvr55GsuXlmTvvN27-MokpPJf8UjP-tM3RKQMLpv-6c")
API_URL = "http://127.0.0.1:8000/run"

@app.post("/run")
async def run_task(task: str = Query(..., description="Plain-English task to execute")):
    """
    Executes a plain-English task using an LLM and returns the result.
    """
    if not OPENAI_TOKEN:
        raise HTTPException(status_code=500, detail="OpenAI token is missing. Set it as an environment variable.")

    headers = {
        "Authorization": f"Bearer {OPENAI_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": task}]
    }

    response = response = requests.post(f"{API_URL}/run", params={"task": task})


    if response.status_code == 200:
        return {"status": "success", "result": response.json()["choices"][0]["message"]["content"]}
    elif response.status_code == 400:
        raise HTTPException(status_code=400, detail="Invalid task format")
    else:
        raise HTTPException(status_code=500, detail="Internal server error while processing task")


@app.get("/read")
async def read_file(path: str = Query(..., description="Path of the file to read")):
    """
    Reads the content of the specified file and returns it.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"status": "success", "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

print("Sending request to FastAPI server...")