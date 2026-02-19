# Makefile for Agentic RAG Sanity Check

PYTHON := python

.PHONY: all sanity clean

# Default target
all: sanity

# -----------------------------------------------------------
# COMMAND: make sanity
# DESCRIPTION: Runs the end-to-end flow and generates artifacts
# -----------------------------------------------------------
sanity:
	@echo "--------------------------------------"
	@echo " Running Sanity Check..."
	@echo "--------------------------------------"
	$(PYTHON) sanity_check.py

# -----------------------------------------------------------
# COMMAND: make verify
# DESCRIPTION: Helper to run the provided judge script locally
# -----------------------------------------------------------
verify: sanity
	@echo "--------------------------------------"
	@echo "  Running Judge Verification..."
	@echo "--------------------------------------"
	$(PYTHON) scripts/verify_output.py artifacts/sanity_output.json

# Cleanup
clean:
	rm -rf artifacts
	rm -rf __pycache__
	rm -f sanity_doc.txt
