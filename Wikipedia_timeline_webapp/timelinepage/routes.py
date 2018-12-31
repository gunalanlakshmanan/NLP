from flask import render_template, url_for, redirect
from timelinepage import app, db
from timelinepage.timeline import timeline
from timelinepage.models import User
from timelinepage.input import InputForm

@app.route("/", methods=['GET', 'POST'])
def input():
    form = InputForm()
    if form.validate_on_submit():
        db.drop_all()
        db.create_all()
        input = User(articlename=form.articlename.data, timelinenumber=form.timelinenumber.data)
        db.session.add(input)
        db.session.commit()
        return redirect(url_for('output'))
    return render_template('input.html', title='Input', form=form)


@app.route("/output",methods=['GET', 'POST'])
def output():
    input = User.query.first()
    word = input.articlename
    n = input.timelinenumber
    sentences = timeline(word, n)
    return render_template('output.html', title='output', sentences=sentences)

