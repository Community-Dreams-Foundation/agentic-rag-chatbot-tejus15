install:
	pip install -r requirements.txt

run:
	streamlit run app.py

sanity:
	python scripts/sanity_check.py
