# Market Minds Insights Hub

## Project Overview

**Market Minds Insights Hub** is a comprehensive project that combines web scraping, data analysis, MySQL integration, and an interactive Power BI dashboard to provide valuable insights into the stock market. The project focuses on top stocks sourced from the screener website, offering a user-friendly interface to explore key financial metrics, market trends, and dynamic visualizations for informed decision-making.

## Project Components

### 1. Data Collection and Cleaning

The project kicks off with web scraping using Python's BeautifulSoup library to extract valuable information about top stocks. The collected data includes essential metrics such as Current Market Price, Price to Earning, Market Capitalization, Dividend Yield, Net Profit, Quarterly Profit Growth, Sales, Quarterly Sales Growth, and Return On Capital Employed.

The data is meticulously cleaned to ensure accuracy and reliability, involving the removal of duplicates and filtering out irrelevant values. The cleaned dataset is then stored in a MySQL database, laying the foundation for subsequent analysis.

### 2. Exploratory Data Analysis (EDA)

Data analysis is performed using Python's Matplotlib library to create insightful visualizations. The EDA phase includes:

- Visualization of top stocks by Current Market Price, Net Profit, and Market Capitalization using bar charts.
- Distribution of Quarterly Profit Growth through a pie chart.
- Comparison of Sales and Net Profit via a bar chart.
- Exploration of the relationship between Return On Capital Employed and Profit Growth using a grouped bar chart.

### 3. Power BI Dashboard

The insights derived from the analysis are seamlessly integrated into an interactive Power BI dashboard. This dashboard provides a user-friendly interface for dynamic exploration of the dataset, enhancing the overall user experience.

### 4. Unique Features

#### Animated Bull and Bear

- The project incorporates an innovative animated bull and bear to represent market sentiment.
- The bull, dressed in a green suit, signifies a bullish market.
- The bear, in red attire, represents a bearish market.

#### Tooltip Enhancements

- Tooltips in the Power BI dashboard include animated bull and bear businessmen, providing real-time insights into market sentiment.
  
## Getting Started

To replicate or build upon this project, follow these steps:

1. Clone the repository.
2. Set up the required Python environment using `requirements.txt`.
3. Run the web scraping script to collect stock data.
4. Clean the data and store it in a MySQL database.
5. Perform exploratory data analysis using the provided Python scripts.
6. Integrate insights into a Power BI dashboard for an interactive experience.

## Conclusion

**Market Minds Insights Hub** is a holistic project that seamlessly integrates web scraping, data analysis, and visualization to offer a comprehensive understanding of top stocks. The interactive Power BI dashboard, along with unique features like animated bull and bear visuals, enhances the user experience and provides valuable insights into market trends.

*To view the live Power BI dashboard, visit [Market Minds Insights Hub on Power BI](#insert_link_here).*
