import subprocess
import json
from datetime import datetime
from pathlib import Path
import sqlite3
import openai
import os
import base64
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def run_command(command: list):
    """Executes a shell command and returns the output."""
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

def count_wednesdays(file_path: str, output_path: str):
    """Counts the number of Wednesdays in a list of dates."""
    with open(file_path, 'r') as file:
        dates = file.readlines()
    wednesday_count = sum(1 for date in dates if datetime.strptime(date.strip(), '%Y-%m-%d').weekday() == 2)
    with open(output_path, 'w') as file:
        file.write(str(wednesday_count))

def sort_contacts(input_path: str, output_path: str):
    """Sorts contacts by last name, then first name."""
    with open(input_path, 'r') as file:
        contacts = json.load(file)
    contacts.sort(key=lambda x: (x['last_name'], x['first_name']))
    with open(output_path, 'w') as file:
        json.dump(contacts, file, indent=2)

def extract_ticket_sales(db_path: str, output_path: str):
    """Extracts total sales for 'Gold' ticket type from SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0
    conn.close()
    with open(output_path, 'w') as file:
        file.write(str(total_sales))

def extract_email_sender(input_path: str, output_path: str):
    """Extracts sender's email address from an email file using an LLM."""
    with open(input_path, 'r') as file:
        email_content = file.read()
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the sender's email address."},
                  {"role": "user", "content": email_content}]
    )
    sender_email = response["choices"][0]["message"]["content"].strip()
    
    with open(output_path, 'w') as file:
        file.write(sender_email)

def extract_credit_card_number(image_path: str, output_path: str):
    """Extracts credit card number from an image using an LLM."""
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "Extract the credit card number from the provided image."},
                  {"role": "user", "content": f"Image data: {encoded_image}"}]
    )
    card_number = response["choices"][0]["message"]["content"].strip()
    
    with open(output_path, 'w') as file:
        file.write(card_number.replace(" ", ""))

def find_most_similar_comments(input_path: str, output_path: str):
    """Finds the most similar pair of comments using embeddings."""
    with open(input_path, 'r') as file:
        comments = file.readlines()
    
    comments = [c.strip() for c in comments if c.strip()]
    embeddings = [
        openai.Embedding.create(
            model="text-embedding-ada-002",
            input=comment
        )["data"][0]["embedding"]
        for comment in comments
    ]
    
    similarity_matrix = cosine_similarity(embeddings)
    np.fill_diagonal(similarity_matrix, 0)  # Ignore self-similarity
    
    max_index = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    most_similar_pair = (comments[max_index[0]], comments[max_index[1]])
    
    with open(output_path, 'w') as file:
        file.write("\n".join(most_similar_pair))

def create_markdown_index(directory: str, output_path: str):
    """Creates an index of Markdown files with their H1 headings."""
    index = {}
    
    for md_file in Path(directory).rglob("*.md"):
        with open(md_file, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("# "):
                    index[md_file.name] = line[2:].strip()
                    break
    
    with open(output_path, "w") as file:
        json.dump(index, file, indent=2)

def extract_recent_log_lines(directory: str, output_path: str):
    """Extracts the first line of the 10 most recent .log files."""
    log_files = sorted(Path(directory).glob("*.log"), key=lambda f: f.stat().st_mtime, reverse=True)[:10]
    recent_lines = []
    
    for log_file in log_files:
        with open(log_file, "r", encoding="utf-8") as file:
            first_line = file.readline().strip()
            if first_line:
                recent_lines.append(first_line)
    
    with open(output_path, "w", encoding="utf-8") as file:
        file.write("\n".join(recent_lines))
