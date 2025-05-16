# Use the official R image
FROM rocker/r-ver:4.4.1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libfontconfig1-dev\
	libpq-dev

# Install R packages (add other required packages)
RUN R -e "install.packages(c('glue', 'shiny', 'DT', 'openxlsx', 'plotly', 'dplyr', 'tidyr', 'ggplot2', 'forcats', 'treemapify', 'rfm', 'lubridate', 'gridExtra', 'maps', 'RPostgres', 'DBI'), repos='https://cloud.r-project.org/')"

# Instala ggsankey diretamente do github
RUN R -e "install.packages('remotes', repos='http://cloud.r-project.org/')" && \
	R -e "remotes::install_github('davidsjoberg/ggsankey')"

# Copy app files
COPY . /app

# Set working directory
WORKDIR /app


EXPOSE 3838

# Run the app
CMD ["R", "-e", "shiny::runApp('/app', host='0.0.0.0', port=3838)"]


