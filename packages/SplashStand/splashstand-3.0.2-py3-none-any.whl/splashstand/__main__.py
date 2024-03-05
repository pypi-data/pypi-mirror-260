import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "splashstand.adapters.app.main:app",
        reload=True,
        reload_includes=["*.py", "*.yml"],
        reload_excludes=[
            "tmp/*",
            "settings/*",
            "theme/*",
        ],
    )
