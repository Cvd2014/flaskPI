from app import app
from flask import render_template, flash, redirect
from app.forms import getPreferences
from app.PersonalityInsights import get_music_preferences
from app.spotify import callApi

def split_up_likes(data):
  for item in data:
    return item


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ciaran'}
    return render_template('index.html', title='Home', user=user)

@app.route('/form', methods=["GET", "POST"])
def personality_check():
    form = getPreferences()
    if form.validate_on_submit():
       	name = form.twittername.data
       	flash('User: {}'.format(
            name))
       	preferences=get_music_preferences(name)

       	flash("{}".format(preferences))
        preferences=split_up_likes(preferences)


        tracks=callApi(preferences)
        flash("{}".format(tracks))

        return redirect('/index')
    return render_template('form.html', title='Get Preferences', form=form)



