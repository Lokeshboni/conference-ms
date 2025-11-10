from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from db import db


payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        amount = request.form.get('amount')
        if not amount:
            flash("Please enter an amount")
        else:
            # Simulate payment confirmation
            db.payments.insert_one({
                "user_id": current_user.id,
                "amount": amount,
                "status": "Completed"
            })
            flash("Payment successful")
    return render_template('payment.html')
