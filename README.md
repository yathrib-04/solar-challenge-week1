# Solar Challenge Week 1

This repository contains the analysis of solar data from various countries, focusing on data profiling, cleaning, and exploratory data analysis.



## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/solar-challenge-week1.git
   cd solar-challenge-week1
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Navigate to the `notebooks` directory
2. Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
3. Open the relevant country's EDA notebook (e.g., `benin_eda.ipynb`)

## Data

The data directory is ignored by git. To work with the notebooks:
1. Download the required dataset
2. Place it in a `data/` directory in the project root
3. Follow the analysis in the corresponding notebook

## Contributing

1. Create a new branch for your work:
   ```bash
   git checkout -b feature-name
   ```
2. Make your changes and commit them
3. Push to your branch and create a Pull Request

## License

MIT License

```bash
git clone https://github.com/yathrib-04/solar-challenge-week1.git
cd solar-challenge-week1
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
