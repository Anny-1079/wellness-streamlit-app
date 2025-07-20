import subprocess

# Start MCP server
mcp_process = subprocess.Popen(["uvicorn", "mcp_server.main:app", "--reload", "--port", "8000"])

# Start Streamlit app
streamlit_process = subprocess.Popen(["streamlit", "run", "streamlit_app/app.py"])

# Wait for both processes
mcp_process.wait()
streamlit_process.wait()
