<!-- Simple way to run tests -->
# First time run test on machine
python -m venv venv
pip install -r requirements.txt

# run when required
source venv/bin/activate
pytest tests --html=reports/report.html
deactivate






