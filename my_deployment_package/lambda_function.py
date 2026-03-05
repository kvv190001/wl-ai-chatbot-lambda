import json
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_PATH = os.path.join(BASE_DIR, "faiss_index")

# Embeddings + LLM
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
llm = ChatGoogleGenerativeAI(temperature=0.5, model="gemini-2.5-flash")

# Connect to FAISS
vector_store = FAISS.load_local(FAISS_PATH, embeddings_model, allow_dangerous_deserialization=True)

# Set up the vectorstore to be the retriever
num_results = 10
retriever = vector_store.as_retriever(search_kwargs={'k': num_results})

# ------------------------
# 🔐 Allowed Origins
# ------------------------
ALLOWED_ORIGINS = {
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://worldlinklabs.ai",
    "dev-wl-labs.xyz",
    "qa-wl-labs.xyz"
}

def check_origin(event):
    """Validate origin header and return a 403 response if invalid."""
    headers = event.get("headers", {}) or {}

    # API Gateway sometimes sends lowercase or uppercase
    origin = headers.get("origin") or headers.get("Origin")

    # No origin → block
    if not origin or origin not in ALLOWED_ORIGINS:
        return {
            "statusCode": 403,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": origin if origin else "",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"message": "Forbidden: Origin not allowed"})
        }
    return None  # means origin is valid

def lambda_handler(event,context):
    # ---------------------------------
    # 🔐 Origin security check
    # ---------------------------------
    origin_check = check_origin(event)
    if origin_check:
        return origin_check  # Block immediately if not allowed
    
    # event["body"] is a JSON string in API Gateway (REST)    
    body = json.loads(event.get("body", "{}"))

    # 🔥 1. Detect warm ping and exit immediately
    if body.get("warm"):
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"status": "warm"})
        }

    # 🔍 Normal request handling
    question = body.get("question", "")

    # retrieve the relevant chunks based on the question asked
    docs = retriever.invoke(question)

    # add all the chunks to 'knowledge'
    knowledge = ""

    for doc in docs:
        knowledge += doc.page_content+"\n\n"

    rag_prompt = f"""
    You are an assistant for WorldLink.
    Your job is to answer questions based solely on the provided knowledge.

    Formatting Rules (VERY IMPORTANT):
    - Use clear paragraph spacing.
    - Use bullet points ("-") when listing multiple items.
    - Each bullet point must be on its own line.
    - Make answers clean and easy to read.
    - If listing organizations, services, or features, ALWAYS use bullet points.
    - NEVER add a blank line between introductory text and bullet points. The first bullet must start on the very next line after the colon.
    - Do NOT use any Markdown formatting (no **, no *, no #, no backticks). Use plain text only.

    However, follow these special rules:

    1. If the user greets you (examples: "hi", "hello", "hey", "how are you"), 
    reply politely and naturally. Do NOT use the knowledge section.

    2. If the user asks "who are you", "what are you",
    or anything about your identity, reply with:
    "I am the WorldLink AI Assistant. I can help answer questions about WorldLink's services, policies, and general information."

    3. For all other questions, you MUST answer ONLY using the information in 'The Knowledge' and not your internal knowledge.

    4. Never mention the knowledge section to the user.

    ---

    The Question: {question}

    The Knowledge: {knowledge}
    """

    response = llm.invoke(rag_prompt)
    answer = response.content

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({"answer": answer})
    }