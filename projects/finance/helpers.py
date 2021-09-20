import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from string import punctuation, ascii_lowercase, ascii_uppercase
from functools import wraps
from datetime import datetime

from cs50 import SQL

db = SQL("sqlite:///finance.db")

# Populating character dicts for quick lookup
PUNC = {}
for p in punctuation:
    PUNC[p] = True

UPPER = {}
for l in ascii_lowercase:
    UPPER[l] = True

LOWER = {}
for l in ascii_uppercase:
    LOWER[l] = True

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def valid_password(password):
    """
    Checks that password uses at least 1 special
    char, 1 uppercase char, 1 lowercase char
    """
    # Intializing variable
    spec = False
    upper = False
    lower = False
    # looping through chars checking for validity
    for c in password:
        try:
            PUNC[c]
            spec = True
            continue
        except KeyError:
            pass
        try:
            UPPER[c]
            upper = True
            continue
        except KeyError:
            pass
        try:
            LOWER[c]
            lower = True
            continue
        except KeyError:
            pass
    # Checking all requirements are true
    if not spec or not upper or not lower:
        return False
    else:
        return True

def get_portfolio():
    user_id = session['user_id']

    # Getting the amount of cash in the users account
    cash = db.execute('Select cash from users where id = ?', session['user_id'])[0]['cash']

    # Intializing the users portfolio, structured as a dictionary
    portfolio = {}
    portfolio['equities'] = []
    portfolio['cash'] = cash
    portfolio['net_worth'] = cash

    # Getting the users stocks
    rows = db.execute("""\
                    SELECT user_stocks.userID, user_stocks.stock, user_stocks.shares, stocks.name
                    FROM user_stocks
                    JOIN stocks ON user_stocks.stock = stocks.ticker
                    WHERE user_stocks.userID = ? AND
                    shares > 0""",
                    user_id)


    for stock in rows:
        # Getting the avg price the user paid for a stock
        stock['price'] = db.execute("""\
        SELECT SUM(transaction_amount) / SUM(num_shares) AS avg from transactions
        WHERE ticker = ? AND
        userID = ?
        """,
        stock['stock'], session['user_id'])[0]['avg']

        # Finding the present value of the users shares
        stock['value'] = lookup(stock['stock'])['price'] * stock['shares']

        portfolio['equities'].append(stock)
        portfolio['net_worth'] += stock['value']

    return portfolio

def valid_form(stock, shares):
    """
    1) shares > 1
    2) a ticker was entered
    if the conditions are met a dictionary with the shares and stock
    information is returned. Else false is returned
    """
    try:
        shares = int(shares)
        return shares > 0 and stock
        if shares > 0 and stock:
            return true
    except ValueError:
        return False

def updatePortfolio(symbol, shares):
    user_id = session['user_id']

    if own_stock(symbol):
        db.execute('UPDATE user_stocks SET shares = shares + ? WHERE userID = ? AND stock = ?', shares, user_id, symbol)
    else:
        db.execute('INSERT INTO user_stocks (userID, stock, shares) VALUES(?, ?, ?)',
        user_id, symbol, shares)

    return None

def own_stock(ticker):
    user_id = session["user_id"]
    # Returning query for stock in the users_id
    return db.execute('SELECT * FROM user_stocks WHERE userID = ? AND stock = ? AND shares > 0', user_id, ticker)


def record_transaction(shares, type, symbol, amount, stock_price):
    user_id = session['user_id']
    #stamping the transaction
    time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    db.execute('INSERT INTO transactions (userID, ticker, transaction_date, num_shares, transaction_type, transaction_amount, stock_price) VALUES(?, ?, ?, ?, ?, ?, ?)',user_id, symbol, time, shares, type, amount, stock_price)
    # Uploading stock information into the db if it's not there already
    if not db.execute('SELECT * FROM stocks WHERE ticker = ?', symbol):
        db.execute('INSERT INTO stocks (ticker, name) VALUES(?, ?)', symbol, lookup(symbol)['name'])
    return None

def updateWallet(transaction_amount):
    """ Updating the amount of money available to the user """
    user_id = session['user_id']
    db.execute('UPDATE users SET cash = cash + ? WHERE id = ?', transaction_amount, user_id)

