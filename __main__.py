import uvicorn
from settings import settings


def main():
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )


if __name__ == "__main__":
    main()
