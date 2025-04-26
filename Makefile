build:
	poetry install

setup:
	echo

unittest:
	poetry run pytest tests

run:
	poetry run streamlit run src/demo5_web_svc/app.py