import streamlit as st
import matplotlib.pyplot as plot
import numpy as np
from main import ask_month_year
from main import load_month_expenses, load_month_budget
from budget_page import get_total_income, get_total_planned, get_budget_categories
from expense_page import get_total_spent

def get_budget_breakdown(month_year):
    month_budget_data = load_month_budget(month_year)
    budget_categories = get_budget_categories(month_year)
    month_expenses = load_month_expenses(month_year)
    budget_breakdown = []

    for budget_category in budget_categories:
        for line in month_budget_data:
            if line["category"] == budget_category:
                planned = line["planned_amount"]

        actual_spending = 0
        for line in month_expenses:
            if line["category"] == budget_category:
                actual_spending += line["amount"]

        remaining = planned - actual_spending

        new_item = [budget_category, planned, actual_spending, remaining]
        budget_breakdown.append(new_item)

    return budget_breakdown
    
def get_planned_amounts(month_year):
    budget_breakdown = get_budget_breakdown(month_year)
    planned_amounts = []
    for line in budget_breakdown:
        planned = line[1]
        planned_amounts.append(planned)

    return planned_amounts

def get_actual_spent(month_year):
    budget_breakdown = get_budget_breakdown(month_year)
    actual_spent = []
    for line in budget_breakdown:
        spent = line[2]
        actual_spent.append(spent)

    return actual_spent


st.subheader("Financial dashboard for:")

month_year = ask_month_year()

st.divider()
inc_col, planned_col, spen_col, remain_col = st.columns(4)

with inc_col:
    total_income = get_total_income(month_year)
    st.info(f"Total Income: ₱{total_income}")
with planned_col:
    total_planned = get_total_planned(month_year)
    if total_planned > total_income:
        st.warning(f"Total Planned: ₱{total_planned}")
    else:
        st.info(f"Total Planned: ₱{total_planned}")
with spen_col:
    total_spent = get_total_spent(month_year)
    if total_spent > total_planned:
        st.warning(f"Actual Spent: ₱{total_spent}")
    else:
        st.info(f"Actual Spent: ₱{total_spent}")
with remain_col:
    remaining_budget = total_income - total_spent
    if remaining_budget < 0 :
        st.warning(f"Remaining Budget: ₱{remaining_budget}")
    else:
        st.info(f"Remaining Budget: ₱{remaining_budget}")



st.divider()

categories = get_budget_categories(month_year)

planned_amounts = get_planned_amounts(month_year)
actual_amounts = get_actual_spent(month_year)

if categories:

    col1, col2 = st.columns(2)
    with col1:
        # Create Matplotlib Figure & Axes
        fig_pie, ax_pie = plot.subplots(figsize=(5, 4))
        ax_pie.pie(planned_amounts, 
            labels=categories,
            autopct="%1.1f%%",)
        ax_pie.axis("equal")
        
        st.pyplot(fig_pie)
    
    with col2:
        x_indices = np.arange(len(categories))
        bar_width = 0.35
        
        fig_bar, ax_bar = plot.subplots(figsize=(5, 4))
        
        ax_bar.bar(x_indices - bar_width / 2, planned_amounts, bar_width, label="Planned", color="#4C72B0")
        ax_bar.bar(x_indices + bar_width / 2, actual_amounts, bar_width, label="Actual", color="#DD8452")
        
        ax_bar.set_ylabel("Amount ($)")
        ax_bar.set_xticks(x_indices)
        ax_bar.set_xticklabels(categories, rotation=45, ha="right")
        ax_bar.legend()
        plot.tight_layout()
        
        st.pyplot(fig_bar)

    table_data = get_budget_breakdown(month_year)

    st.divider()

    st.subheader("Monthly Budget Breakdown")
    st.write("")
    col_ratios = [2, 1.5, 1.5, 1.5, 3]
    header_cols = st.columns(col_ratios)
    for col, header in zip(
        header_cols, ["Category", "Planned Amount", "Actual Spending", "Remaining", "Status"]):
        col.markdown(f"**{header}**")
    for index, row in enumerate(table_data):
        cols = st.columns(col_ratios)
        cols[0].write(row[0])
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(row[3])
        if row[3] < 0:
            cols[4].warning(f"OVER BUDGET by ₱{abs(row[3])}")
        else:
            cols[4].info("On track")

    st.divider()