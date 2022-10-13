# Cost comparison of Agile + Battery vs standard cost

## Summary

- The code gets price tariff data from octopus api and synthetic demand data from a MYSQL database hosted on AWS.  
- Users supply a date, a battery specification and an agile tariff option.  
- For the week commencing on the supplied date, a cost comparison between a fixed tariff and an Agile tariff with a battery.
- The best battery operational strategy is found for the week provided.
- The results generated are presented using Dash, a dashboard found at: **http://127.0.0.1:8050/**

---

## Instructions

### Installation instructions
- Create virtual environment with necessary packages using requirments.txt or oct_test.yml (for pip, use requirementspip.txt)
- If using anaconda, this is done by running: *conda env create -f oct_test.yml*
- Activate environment using: *conda activate oct_test*


### Option 1: Run directly from shell
- Set user parameters in **user_inputs.py**
- Run the following: *python run_cost_comparison.py*
- Results are generated and presented at **http://127.0.0.1:8050/**

### Option 2: Run via jupyter notebook
- Open jupyter notebook using: *jupyter notebook*
- From window that opens in browser, open **Notebook.ipynb**
- Run each cell, modifying user parameters if desired.
- Results are plotted directly in notebook

---
## User parameters
- Start date: Any date/time between *01/01/2020 00:00* and *01/10/2022 00:00* in format *dd/mm/yyyy hh:mm*
- Agile version: Newer agile tariff codes have come along. Choose either *0, 1, 2*. 0 corresponds to *AGILE-18-02-21*, 1 corresponds to *AGILE-22-07-22* and 2 corresponds to *AGILE-22-08-31*. 1 and 2 are not available for more older start date choices (as they didn't exist at the time)
- Bat_capacity: The capacity of the battery can be defined in kWh (must be a positive number)
- ch_max: The maximum charge and discharge power of the battery can be defined in kW (must be a positive number)
- Eff: The round-trip efficiency can be defined between 0 and 1 (1 corresponds to 100% efficiency, i.e., a battery with no losses)



