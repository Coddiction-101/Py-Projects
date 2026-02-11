#!/usr/bin/env python3
"""
Personal Expense Tracker
A real-life expense management system with categories, budgets, and analytics
"""

import json
import os
from datetime import datetime
from collections import defaultdict


class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.categories = ["Food", "Transport", "Entertainment", "Bills", "Shopping", "Health", "Other"]
        self.budget_limits = {}
        self.load_data()
    
    def load_data(self):
        """Load expenses from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    self.expenses = data.get('expenses', [])
                    self.budget_limits = data.get('budgets', {})
                print(f"✓ Loaded {len(self.expenses)} expenses from file")
            except json.JSONDecodeError:
                print("⚠ Error reading file, starting fresh")
                self.expenses = []
        else:
            print("📝 Starting new expense tracker")
    
    def save_data(self):
        """Save expenses to file"""
        data = {
            'expenses': self.expenses,
            'budgets': self.budget_limits
        }
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
        print("✓ Data saved successfully!")
    
    def add_expense(self):
        """Add a new expense"""
        print("\n" + "="*50)
        print("📝 ADD NEW EXPENSE")
        print("="*50)
        
        # Get amount
        while True:
            try:
                amount = float(input("💵 Enter amount: ₹"))
                if amount <= 0:
                    print("⚠ Amount must be positive!")
                    continue
                break
            except ValueError:
                print("⚠ Please enter a valid number!")
        
        # Get category
        print("\nCategories:")
        for i, cat in enumerate(self.categories, 1):
            print(f"  {i}. {cat}")
        
        while True:
            try:
                choice = int(input("Select category (1-7): "))
                if 1 <= choice <= 7:
                    category = self.categories[choice - 1]
                    break
                else:
                    print("⚠ Please select 1-7!")
            except ValueError:
                print("⚠ Please enter a number!")
        
        # Get description
        description = input("📋 Enter description: ").strip()
        if not description:
            description = "No description"
        
        # Get date (default: today)
        date_str = input("📅 Enter date (DD-MM-YYYY) [Press Enter for today]: ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%d-%m-%Y")
        
        # Create expense
        expense = {
            'id': len(self.expenses) + 1,
            'amount': amount,
            'category': category,
            'description': description,
            'date': date_str
        }
        
        self.expenses.append(expense)
        self.save_data()
        
        print(f"\n✅ Expense added successfully! (ID: {expense['id']})")
        
        # Check budget warning
        self.check_budget_warning(category)
    
    def view_all_expenses(self):
        """Display all expenses"""
        if not self.expenses:
            print("\n📭 No expenses recorded yet!")
            return
        
        print("\n" + "="*80)
        print("📊 ALL EXPENSES")
        print("="*80)
        print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<30}")
        print("-"*80)
        
        total = 0
        for exp in self.expenses:
            print(f"{exp['id']:<5} {exp['date']:<12} {exp['category']:<15} ₹{exp['amount']:<9.2f} {exp['description']:<30}")
            total += exp['amount']
        
        print("-"*80)
        print(f"{'TOTAL:':<42} ₹{total:.2f}")
        print("="*80)
    
    def view_by_category(self):
        """Display expenses grouped by category"""
        if not self.expenses:
            print("\n📭 No expenses recorded yet!")
            return
        
        print("\n" + "="*60)
        print("📂 EXPENSES BY CATEGORY")
        print("="*60)
        
        category_totals = defaultdict(float)
        for exp in self.expenses:
            category_totals[exp['category']] += exp['amount']
        
        total = 0
        for category in sorted(category_totals.keys()):
            amount = category_totals[category]
            total += amount
            percentage = (amount / sum(category_totals.values())) * 100
            print(f"{category:<15} ₹{amount:>10.2f}  ({percentage:>5.1f}%)")
        
        print("-"*60)
        print(f"{'TOTAL:':<15} ₹{total:>10.2f}")
        print("="*60)
    
    def monthly_summary(self):
        """Show monthly summary"""
        if not self.expenses:
            print("\n📭 No expenses recorded yet!")
            return
        
        print("\nEnter month (MM-YYYY) [Press Enter for current month]: ", end="")
        month_input = input().strip()
        
        if not month_input:
            month_input = datetime.now().strftime("%m-%Y")
        
        print("\n" + "="*60)
        print(f"📅 MONTHLY SUMMARY - {month_input}")
        print("="*60)
        
        monthly_expenses = [exp for exp in self.expenses if exp['date'].endswith(month_input)]
        
        if not monthly_expenses:
            print(f"📭 No expenses found for {month_input}")
            return
        
        category_totals = defaultdict(float)
        total = 0
        
        for exp in monthly_expenses:
            category_totals[exp['category']] += exp['amount']
            total += exp['amount']
        
        print(f"\nTotal Expenses: {len(monthly_expenses)}")
        print(f"Total Amount: ₹{total:.2f}")
        print(f"Average per expense: ₹{total/len(monthly_expenses):.2f}")
        print("\nCategory Breakdown:")
        
        for category in sorted(category_totals.keys()):
            amount = category_totals[category]
            percentage = (amount / total) * 100
            bar = "█" * int(percentage / 2)
            print(f"{category:<15} ₹{amount:>8.2f} {bar} {percentage:.1f}%")
        
        print("="*60)
    
    def set_budget(self):
        """Set budget limit for a category"""
        print("\n" + "="*50)
        print("💰 SET BUDGET LIMIT")
        print("="*50)
        
        print("\nCategories:")
        for i, cat in enumerate(self.categories, 1):
            current = self.budget_limits.get(cat, "Not set")
            if current != "Not set":
                current = f"₹{current}"
            print(f"  {i}. {cat:<15} (Current: {current})")
        
        while True:
            try:
                choice = int(input("\nSelect category (1-7): "))
                if 1 <= choice <= 7:
                    category = self.categories[choice - 1]
                    break
                else:
                    print("⚠ Please select 1-7!")
            except ValueError:
                print("⚠ Please enter a number!")
        
        while True:
            try:
                limit = float(input(f"Enter budget limit for {category}: ₹"))
                if limit < 0:
                    print("⚠ Budget must be positive!")
                    continue
                break
            except ValueError:
                print("⚠ Please enter a valid number!")
        
        self.budget_limits[category] = limit
        self.save_data()
        print(f"✅ Budget set for {category}: ₹{limit:.2f}")
    
    def check_budget_warning(self, category):
        """Check if expense exceeds budget"""
        if category not in self.budget_limits:
            return
        
        category_total = sum(exp['amount'] for exp in self.expenses if exp['category'] == category)
        limit = self.budget_limits[category]
        
        if category_total > limit:
            overspend = category_total - limit
            print(f"\n⚠ WARNING: {category} budget exceeded by ₹{overspend:.2f}!")
        elif category_total > limit * 0.8:
            remaining = limit - category_total
            print(f"\n⚠ ALERT: {category} budget 80% used. ₹{remaining:.2f} remaining.")
    
    def search_expenses(self):
        """Search expenses by date range"""
        print("\n" + "="*50)
        print("🔍 SEARCH EXPENSES")
        print("="*50)
        
        start_date = input("Enter start date (DD-MM-YYYY): ").strip()
        end_date = input("Enter end date (DD-MM-YYYY): ").strip()
        
        # Convert dates for comparison
        try:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            end = datetime.strptime(end_date, "%d-%m-%Y")
        except ValueError:
            print("⚠ Invalid date format!")
            return
        
        results = []
        for exp in self.expenses:
            exp_date = datetime.strptime(exp['date'], "%d-%m-%Y")
            if start <= exp_date <= end:
                results.append(exp)
        
        if not results:
            print("\n📭 No expenses found in this date range")
            return
        
        print(f"\n📊 Found {len(results)} expenses")
        print("-"*80)
        print(f"{'ID':<5} {'Date':<12} {'Category':<15} {'Amount':<10} {'Description':<30}")
        print("-"*80)
        
        total = 0
        for exp in results:
            print(f"{exp['id']:<5} {exp['date']:<12} {exp['category']:<15} ₹{exp['amount']:<9.2f} {exp['description']:<30}")
            total += exp['amount']
        
        print("-"*80)
        print(f"{'TOTAL:':<42} ₹{total:.2f}")
    
    def delete_expense(self):
        """Delete an expense by ID"""
        if not self.expenses:
            print("\n📭 No expenses to delete!")
            return
        
        self.view_all_expenses()
        
        try:
            exp_id = int(input("\nEnter expense ID to delete (0 to cancel): "))
            if exp_id == 0:
                return
            
            for i, exp in enumerate(self.expenses):
                if exp['id'] == exp_id:
                    confirm = input(f"Delete expense '{exp['description']}'? (y/n): ").lower()
                    if confirm == 'y':
                        self.expenses.pop(i)
                        self.save_data()
                        print("✅ Expense deleted successfully!")
                    return
            
            print("⚠ Expense ID not found!")
        except ValueError:
            print("⚠ Invalid ID!")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("💰 PERSONAL EXPENSE TRACKER")
        print("="*50)
        print("1. 📝 Add Expense")
        print("2. 📊 View All Expenses")
        print("3. 📂 View by Category")
        print("4. 📅 Monthly Summary")
        print("5. 🔍 Search Expenses")
        print("6. 💰 Set Budget Limit")
        print("7. 🗑️  Delete Expense")
        print("8. 🚪 Exit")
        print("="*50)
    
    def run(self):
        """Main application loop"""
        print("\n🎉 Welcome to Personal Expense Tracker!")
        
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-8): ").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_all_expenses()
            elif choice == '3':
                self.view_by_category()
            elif choice == '4':
                self.monthly_summary()
            elif choice == '5':
                self.search_expenses()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.delete_expense()
            elif choice == '8':
                print("\n✅ Thank you for using Expense Tracker!")
                print("💾 All data saved. Goodbye! 👋")
                break
            else:
                print("⚠ Invalid choice! Please select 1-8")


if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
