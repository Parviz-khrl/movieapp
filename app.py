from flask import Flask, render_template, request, redirect, url_for, flash
from forsearch import searchreq
from datetime import timedelta

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=31)
app.secret_key = "d273fd202ae36a79dd36f160616859903861e535d49b44793b1d2930b05ff33a"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search', methods=['POST'])
def search():
    title = request.form['title']
    year = request.form.get('year')
    type = request.form.get('type')
    genre = request.form.get('genre')  
    
    try:
        jsonresp = searchreq(title, year, type, genre) 
        results = jsonresp.get("Search")
        
        if not results:
            flash('No results found. Try again with different keywords.')
            return redirect(url_for('index'))

        # Checking if the user input for genre, year, or type is invalid
        if genre and not any(result['Genre'].lower().startswith(genre.lower()) for result in results):
            flash(f"No movies found in the {genre} genre. Please try again with different parameters.")
            return redirect(url_for('index'))

        if year and not any(result['Year'] == year for result in results):
            flash(f"No movies found from the year {year}. Please try again with different parameters.")
            return redirect(url_for('index'))

        if type and not any(result['Type'].lower() == type.lower() for result in results):
            flash(f"No {type} found. Please try again with different parameters.")
            return redirect(url_for('index'))

        # If all checks pass, display the search results
        return render_template("search_results.html", results=results)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.errorhandler(404)
def notfound(error):
    return render_template('notfound.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
