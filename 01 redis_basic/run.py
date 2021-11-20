import uvicorn


def main(host: str = '0.0.0.0', port: int = 8000):
    uvicorn.run(
        'main:app',
        host=host,
        port=port,
        reload=True,
    )


if __name__ == '__main__':
    main()
