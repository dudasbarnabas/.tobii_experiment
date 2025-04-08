# .tobii_experiment

# Clone and enter project
git clone https://github.com/dudasbarnabas/.tobii_experiment.git

# Create virtual environment
python -m venv venv
pip install -r requirements.txt
pip install -e .

# Run
python -m src.main