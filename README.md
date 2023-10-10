# Convert EMI internal forecast formats

This converts forecasts in csv files from the format used for EMI's web pages to the format required for EMI's app input.

Example usage:

```bash
python3 convert_forecast.py --output-file out.csv --forecast-time "2023-12-23" input.csv
```

This will read a forecast from the file `input.csv`, and write to the file `out.csv`. The first day of the forecast will be the 23. of December 2023 (2023-12-23). Any problems when converting the forecast will be written in the terminal.
