from fastapi import FastAPI, HTTPException
import os

app = FastAPI()

@app.post("/run")
def run_task(task: str):
    try:
        # Placeholder for task execution logic
        return {"status": "success", "message": f"Executed task: {task}"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task input")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

@app.get("/read")
def read_file(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(path, "r") as file:
        content = file.read()
    return {"status": "success", "content": content}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
