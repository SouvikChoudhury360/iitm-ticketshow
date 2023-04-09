from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import venue, show, bookings, ratings
from datetime import datetime
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    venues = venue.query.all()

    shows = []
    for thisvenue in range(1,100):
        showList = show.query.filter_by(venue_id=thisvenue)
        shows.append(showList)
    return render_template('dashboard.html', user=current_user, venues = venues, shows = shows)

@main.route('/adminDashboard')
@login_required
def adminDashboard():
    venues = venue.query.all()
    shows = []
    for thisvenue in range(1,100):
        showList = show.query.filter_by(venue_id=thisvenue)
        shows.append(showList)
    return render_template('admin_dashboard.html', venues = venues, shows = shows)

@main.route('/createVenue')
@login_required
def createVenue():
    return render_template('create_venue.html')

@main.route('/createVenue', methods=['POST'])
def createVenue_post():
    address = request.form.get('address')
    name = request.form.get('name')
    capacity = request.form.get('capacity')
    new_venue = venue(name=name, address= address, capacity=capacity)
    db.session.add(new_venue)
    db.session.commit()
    flash('Venue Created!')
    return redirect(url_for('main.adminDashboard'))

@main.route("/venue/<int:venue_id>/edit", methods=['GET','POST'])
@login_required
def editVenue(venue_id):
    thisvenue = venue.query.get_or_404(venue_id)
    if request.method == 'POST':
        thisvenue.name = request.form['name']
        thisvenue.address = request.form['address']
        thisvenue.capacity = request.form['capacity']
        db.session.commit()
        flash('Your venue has been updated!')
        return redirect(url_for('main.adminDashboard'))
    return render_template('edit_venue.html', venue=thisvenue)

@main.route("/venue/<int:venue_id>/delete", methods=['GET', 'POST'])
@login_required
def deleteVenue(venue_id):
    thisvenue = venue.query.get_or_404(venue_id)
    db.session.delete(thisvenue)
    db.session.commit()
    return redirect(url_for('main.adminDashboard'))

@main.route('/<int:venue_id>/createShow', methods=['GET', 'POST'])
@login_required
def createShow(venue_id):
    if request.method == 'POST':
        thisvenue = venue.query.filter_by(id=venue_id).first()
        title = request.form['title']
        tags =  request.form['tags']
        #date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M')
        ticket_price = request.form['ticket_price']
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        thisshow = show(title=title, tags=tags, ticket_price=ticket_price, starting_time=start_time, ending_time=end_time, capacity=thisvenue.capacity, venue_id=thisvenue.id)
        db.session.add(thisshow)
        db.session.commit()
        flash('Show Created!')
        return redirect(url_for('main.adminDashboard'))   
    if request.method == 'GET':
        thisvenue = venue.query.filter_by(id=venue_id).first()
        return render_template('create_show.html', venue=thisvenue)

@main.route("/show/<int:show_id>/delete", methods=['GET', 'POST'])
@login_required
def deleteShow(show_id):
    thisshow = show.query.get_or_404(show_id)
    db.session.delete(thisshow)
    db.session.commit()
    return redirect(url_for('main.adminDashboard'))

@main.route("/show/<int:show_id>/edit", methods=['GET','POST'])
@login_required
def editShow(show_id):
    thisshow = show.query.get_or_404(show_id)
    thisvenue = venue.query.get_or_404(thisshow.venue_id)
    if request.method == 'POST':
        thisshow.title = request.form['title']
        thisshow.tags = request.form['tags']
        thisshow.ticket_price = request.form['ticket_price']
        thisshow.starting_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        thisshow.ending_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
        db.session.commit()
        flash('Your show has been updated!')
        return redirect(url_for('main.adminDashboard'))
    return render_template('edit_show.html', show=thisshow, venue=thisvenue)

@main.route('/booking/<int:show_id>', methods=['GET'])
def booking_get(show_id):
    thisshow = show.query.filter_by(id=show_id).first()
    return render_template('booking.html', show=thisshow)

@main.route('/booking/<int:show_id>', methods=['POST'])
def booking_post(show_id):
    count = request.form.get('count')
    new_booking = bookings(show_id=show_id, count=int(count), user_id=int(current_user.id))
    thisshow = show.query.get_or_404(show_id)
    if thisshow.capacity < int(count) :
        return redirect(url_for('main.dashboard'))
    thisshow.capacity = thisshow.capacity - int(count)
    db.session.add(new_booking)
    db.session.commit()
    flash('Booking Created!')
    return redirect(url_for('main.dashboard'))

@main.route('/mybookings', methods= ['GET'])
def mybookings():
    bookingsList = bookings.query.filter_by(user_id=current_user.id)
    showlist = {}
    for thisbooking in bookingsList:
        thisshow = show.query.filter_by(id=thisbooking.show_id).first()
        showlist[thisbooking.id] = thisshow
    return render_template('my_bookings.html', bookings=bookingsList, shows=showlist)

@main.route('/rating/<int:show_id>', methods=['POST'])
def rating_post(show_id):
    rating = request.form.get('rating')
    new_rating = ratings(show_id=show_id, rating=int(rating), user_id=int(current_user.id))
    db.session.add(new_rating)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/rating/<int:show_id>', methods=['GET'])
def rating_get(show_id):
    thisshow = show.query.filter_by(id=show_id).first()
    ratings_list = ratings.query.filter_by(show_id=thisshow.id)
    for thisrating in ratings_list:
        if thisrating.show_id == thisshow.id and thisrating.user_id == current_user.id:
            return render_template('already_rated.html')
    return render_template('rating_form.html', show=thisshow)


@main.route('/analytics/<int:show_id>', methods=['GET'])
def analytics(show_id):
    thisshow = show.query.filter_by(id=show_id).first()
    ratings_list = ratings.query.all()
    rating_list = [0,0,0,0,0]
    for rating in ratings_list:
        if rating.show_id == show_id:
            rating_list[rating.rating-1] += 1
    #print(rating_list)
    return render_template('analytics.html', rating_list=rating_list, show=thisshow)

@main.route('/search', methods=['GET'])
def search_landing_screen():
    show_list = show.query.all()
    return render_template('search_shows.html',shows= show_list)

@main.route('/search/shows', methods=['GET', 'POST'])
def search_shows():
    search_text = request.form['show_search']
    search = "%{}%".format(search_text)
    showlist = show.query.filter(show.title.like(search)).all()
    showtags = show.query.filter(show.tags.like(search)).all()
    return render_template('search_shows.html',shows= showlist, showtags=showtags)
