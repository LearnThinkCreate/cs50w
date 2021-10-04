import os
import logging

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import *

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = get_portfolio()

    return render_template('index.html', portfolio=portfolio)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock = request.form.get('stock')
        shares = request.form.get('shares')

        # Validating form information
        if not valid_form(stock, shares):
            return apology("The stock ticker or number of shares entered is invalid")

        # Getting user id
        user_id = session['user_id']

        # Geting quote
        quote = lookup(stock)

        if quote:
            price = quote['price']
            cost = price * int(shares)
            balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
            if balance > cost:
                # record transaction
                record_transaction(shares, 'buy', stock, cost, price)
                # Updating the users Portfolio
                updatePortfolio(stock, int(shares))
                # Subtract funds from wallet
                updateWallet(-cost)
                return redirect('/')
            else:
                return apology("You don't have enough funds")
        else:
            return apology("Stock not found")
    else:
        return render_template('buy.html')


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("""\
    SELECT ticker, num_shares, stock_price, transaction_date, transaction_type
    FROM transactions
    WHERE userID = ?
    """, session['user_id'])

    return render_template('history.html', history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").lower())

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        ticker = request.form.get('quote')
        try:
            stock = lookup(ticker)
            price = stock['price']
            name = stock['name']
            symbol = stock['symbol']
            return render_template('quoted.html', price=price, name=name, symbol=symbol)
        except:
            return apology("Invalid ticker", 400)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        # Get variables
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)
        # Ensure password was submitted
        elif not password or not confirmation:
            return apology("must provide password", 403)
        elif len(password) < 6:
            return apology("password is not log enough", 403)
        elif not valid_password(password):
            return apology("password must contain 1 uppercase letter, 1 lowercase letter and 1 special character")

        # Query database for username -- case sensative
        rows = db.execute("SELECT * FROM users WHERE username = ?", username.lower())

        # Ensure username is unique
        if len(rows) != 0:
            return apology("Username is already taken", 403)

        # Ensure that the confirmation
        if password != confirmation:
            return apology("Passwords must match", 403)

        # Inserting the user into the db
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))

        return redirect('/')
    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        stock = request.form.get('stock')
        shares = request.form.get('shares')

        # Validating form information
        if not valid_form(stock, shares):
            return apology("The stock ticker or number of shares entered is invalid")

        # Getting user id
        user_id = session['user_id']

        # Geting quote
        quote = lookup(stock)

        if quote:
            # Ensuring user owns stock
            if not own_stock(stock):
                return apology("You don't own this stock")

            price = quote['price']
            profit = price * int(shares)
            shares_owned = db.execute("""\
            SELECT shares
            FROM user_stocks
            WHERE id = ? AND stock = ?
            """, user_id, stock)[0]['shares']

            if shares_owned > int(shares):
                # record transaction
                record_transaction(-int(shares), 'sell', stock, profit, price)
                # Updating the users Portfolio
                updatePortfolio(stock, -int(shares))
                # Subtract funds from wallet
                updateWallet(profit)
                return redirect('/')
            else:
                return apology(f"You can only sell up to {shares_owned} shares")
        else:
            return apology("Stock not found")
    else:
        return render_template('sell.html')



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
