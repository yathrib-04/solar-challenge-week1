# Solar Challenge Week 1

## Overview
This project analyzes and compares solar energy data from Benin, Togo, and Sierra Leone. The goal is to clean, explore, and compare solar potential across these countries using Python and Jupyter Notebooks.

## Project Structure
```
solar-challenge-week1/
├── app/                 # Streamlit application
├── data/               # Raw and processed data files
├── notebooks/          # Jupyter notebooks for analysis
├── scripts/            # Utility scripts
├── src/               # Source code
├── tests/             # Unit tests
└── .github/           # GitHub Actions workflows
```

## Data Sources
- Benin (Malanville)
- Togo (Dapaong)
- Sierra Leone (Bumbuna)

## Prerequisites
- Python 3.8 or higher
- Git
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/solar-challenge-week1.git
cd solar-challenge-week1
```

2. Create and activate a virtual environment:
   - Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Analysis
1. Start Jupyter Notebook:
```bash
jupyter notebook
```
2. Open and run the notebooks in the `notebooks/` directory in order.

### Running the Streamlit App
```bash
streamlit run app/app.py
```

### Running Tests
```bash
pytest tests/
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Testing
- Write unit tests for new features
- Run tests before submitting PRs
- Maintain test coverage

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Progress
- [x] Data cleaning and EDA for each country
- [x] Cross-country comparison
- [ ] Further statistical analysis and visualization improvements

## Contributors
- Teyiba Aman

## Acknowledgments
- Thanks to all contributors and reviewers
- Special thanks to the data providers
