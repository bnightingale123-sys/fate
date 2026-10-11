from mcp_server import server
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "mcp_server_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
