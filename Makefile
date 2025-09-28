.PHONY: help install test clean run status

help:
	@echo "AstrOS Stage 1 Development Commands:"
	@echo "  install     - Set up development environment"
	@echo "  test        - Run tests"
	@echo "  run         - Run agent in interactive mode"
	@echo "  status      - Show project status"
	@echo "  clean       - Clean build artifacts"

install:
	@echo "Setting up AstrOS development environment..."
	python -m venv venv
	./venv/Scripts/pip install -e ".[dev]"
	@echo "✅ Development environment ready"
	@echo "Activate with: venv\\Scripts\\activate"

test:
	./venv/Scripts/python -m pytest tests/ -v

run:
	./venv/Scripts/python -m astros.cli interactive

status:
	./venv/Scripts/python -m astros.cli status

clean:
	rmdir /s /q build 2>nul || echo "No build directory"
	rmdir /s /q dist 2>nul || echo "No dist directory"
	rmdir /s /q venv 2>nul || echo "No venv directory"
	for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"