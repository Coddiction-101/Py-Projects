
"""PERSONAL EXPENSE TRACKER"""
# A personal expense management system with categories, budgets and analytics

import json
import os
from datetime import datetime
from collections import defaultdict


class expenseTracker:
    def __init__(self, filaname = "expenses.json"):
        self.filename = filename
        self.expenses = []
        self.categories = ["Food", "Entertainment", "Health", "Other", "Bills", "Shopping", "Transport"]
        self.budget_limits = {}
        self.load_date()
        
         
