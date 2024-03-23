import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from scipy.optimize import fsolve

@st.cache_data
def proposedtax2025(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 18200), (18201, 45000), (45001, 135000), (135001, 190000), (190001, float('inf'))]
    tax_rates = [0, 0.16, 0.30, 0.37, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def stage3tax2025(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 18200), (18201, 45000), (45001, 200000), (200001, float('inf'))]
    tax_rates = [0, 0.19, 0.30, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def medicare2025(taxable_income):
    lower_limit = 24276
    upper_limt = 30345
    if taxable_income < lower_limit:
        return 0.0

    # Calculate the Medicare Levy for income above the lower threshold
    medicare_levy = (taxable_income - lower_limit) * 0.015

    # Apply the Medicare Levy Surcharge if applicable
    if taxable_income >=  upper_limt:
        medicare_levy_rate = 0.02
        medicare = taxable_income * medicare_levy_rate
        medicare_levy += medicare
    return medicare_levy

def proposed_medicare2025(taxable_income):
    lower_limit = 26000
    upper_limt = 32500
    if taxable_income < lower_limit:
        return 0.0

    # Calculate the Medicare Levy for income above the lower threshold
    medicare_levy = (taxable_income - lower_limit) * 0.015

    # Apply the Medicare Levy Surcharge if applicable
    if taxable_income >=  upper_limt:
        medicare_levy_rate = 0.02
        medicare = taxable_income * medicare_levy_rate
        medicare_levy += medicare
    return medicare_levy

def nrtax2025(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 200000), (200001, float('inf'))]
    tax_rates = [0.30, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def proposed_nrtax2025(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 135000), (135001, 190000), (190001, float('inf'))]
    tax_rates = [0.30, 0.37, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def hmtax2025(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 45000), (45001, 200000), (200001, float('inf'))]
    tax_rates = [0.15, 0.30, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def proposed_hmtax2025(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 45000), (45001, 135000), (135001, 190000), (190001, float('inf'))]
    tax_rates = [0.15, 0.30, 0.37, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def lito(taxable_income):
    # ATO low income tax offset calculation
    if taxable_income <= 37000:
        lito = 700
    elif 37501 <= taxable_income <= 45000:
        lito = 700 - ((taxable_income - 37500) * 0.05)
    elif 45001 <= taxable_income <= 66666:
        lito = 325 - ((taxable_income - 45000) * 0.015)
    else:
        lito = 0
    return max(lito, 0)

def litmo(taxable_income):
    # ATO low income tax offset calculation
    if taxable_income <= 37000:
        litmo = 675
    elif 37501 <= taxable_income <= 48000:
        litmo = min(675 + ((taxable_income - 37500) * 0.05),1500)
    elif 45001 <= taxable_income <= 90000:
        litmo = 1500 
    elif 90001 <= taxable_income <= 126000:
        litmo = 1500 - ((taxable_income - 90001) * 0.3)
    else:
        litmo = 0
    return max(litmo, 0)

def prior_tax2024(taxable_income):
    # https://www.aph.gov.au/Parliamentary_Business/Bills_Legislation/bd/bd2324a/24bd42a
    tax_brackets = [(0, 18200), (18201, 45000), (45001, 120000), (120001, 180000), (180001, float('inf'))]
    tax_rates = [0, 0.19, 0.325, 0.37, 0.45]
    
    tax = 0.0
    for i, (lower, upper) in enumerate(tax_brackets):
        if taxable_income > upper:
            tax += (upper - lower) * tax_rates[i]
        elif taxable_income > lower:
            tax += (taxable_income - lower) * tax_rates[i]
            break 
    return tax

def tax_chart():
    taxable_income_range = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 130000, 140000, 150000, 160000, 170000, 180000, 190000, 200000, 210000, 220000, 230000]
    prior_liability = []
    tax_liability = []
    proposed_tax_liability =[]

    for i in taxable_income_range:
        prior_tax = int(prior_tax2024(i))
        tax_range = int(stage3tax2025(i))
        proposed_tax_range = int(proposedtax2025(i))
        prior_liability.append(prior_tax)
        tax_liability.append(tax_range)
        proposed_tax_liability.append(proposed_tax_range)

    return taxable_income_range, prior_liability, tax_liability, proposed_tax_liability

def goal_seek(target_litmo):

    def equation(taxable_income):
        return litmo(taxable_income) - target_litmo

    # Initial guess for taxable income (adjust as needed)
    initial_guess = None

    # Using fsolve to find the root of the equation
    result = fsolve(equation, initial_guess)

    return result[0]

def load_data(file_path):
    return pd.read_csv(file_path)

def animate(i, x_data, y_data):
    plt.cla()  # Clear the current axis
    plt.plot(x_data[:i+1], y_data[:i+1])
