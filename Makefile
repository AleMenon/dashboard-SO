PYTHON=python3
MAIN=main.py

run:
	@$(PYTHON) $(MAIN)

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +

.PHONY: run clean
