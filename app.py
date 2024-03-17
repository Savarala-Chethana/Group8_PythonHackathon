from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file, make_response

from flask import Flask,render_template,request
import mysql.connector
   
import matplotlib.pyplot as plt
import base64
import pandas as pd

from io import BytesIO

import uuid
num = uuid.uuid1()



app=Flask(__name__)
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Chethu$13",
    database="flask"
)

mycursor=mydb.cursor()

# Sample flight and hotel data stored in memory (replace with your actual data)
flights = []
hotels = []
 
# Fetch flight and hotel data from the database
def fetch_flight_data():
    mycursor.execute('SELECT * FROM Flights')
    return [{"FlightNumber": flight[0], "FlightName": flight[1],"StartPlace": flight[2],"DestPlace": flight[3],"StartTime": flight[4],"DestTime": flight[5],"Price": flight[6]} for flight in mycursor.fetchall()]
 
def fetch_hotel_data():
    mycursor.execute('SELECT * FROM Hotels')
    return [{"HotelId": hotel[0], "HotelName": hotel[1],"HotelPlace": hotel[2], "HotelAddress": hotel[3],"Price": hotel[4]} for hotel in mycursor.fetchall()]

# Home page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/signupsubmit',methods=['GET','POST'])
def signup_submit():
    if request.method == 'POST':
        firstName=request.form.get('firstname')
        lastName=request.form.get('lastname')
        email=request.form.get('username')
        pswd=request.form['password']
    
        query="insert into Login_Credentials VALUES(%s,%s,%s,%s)"
        data=(email,firstName,lastName,pswd)
        mycursor.execute(query,data)
        mydb.commit()
        return render_template('Login.html')
    return render_template('Signup.html')

@app.route('/signup')
def signup():
    return render_template('Signup.html')

@app.route('/loginsubmit',methods=['POST'])
def login_submit():
    
    if request.method == 'POST':
        email=request.form.get('username')
        pswd=request.form.get('password')

        mycursor.execute("SELECT password FROM Login_Credentials WHERE username = %s", [email])
        user = mycursor.fetchone()
        print(user)
        if user:
            if pswd==user[0]:
                return render_template('dashboard.html')
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'User not found'
            return render_template('login.html', error=error)
 
    return render_template('login.html')

@app.route('/contactus')
def contactus_page():
    return render_template('ContactUs.html')

@app.route('/aboutus')
def aboutus_page():
    return render_template('AboutUs.html')

@app.route('/logout')
def logout():
    return render_template('Home.html')

@app.route('/services')
def services():
    return render_template('Services.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin')
def admin():
    return render_template('admin_main.html')

@app.route('/adminn')
def adminn():
    return render_template('admin_login.html')

@app.route('/adminflights')
def admin_flights():
    query="select * from Flights"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template('admin_flights.html',sqldata=data)

@app.route('/adminhotels')
def admin_hotels():
    query="select * from Hotels"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template('admin_hotels.html',sqldata=data)

@app.route('/adminlogin',methods=['POST'])
def admin_login():
    if request.method == 'POST':
        username=request.form.get('username')
        pswd=request.form.get('password')

        mycursor.execute("SELECT password FROM admin WHERE username = %s", [username])
        user = mycursor.fetchone()
        print(user)
        if user:
            if pswd==user[0]:
                global flights, hotels
                flights = fetch_flight_data()
                hotels = fetch_hotel_data()
                return render_template('admin_main.html', flights=flights, hotels=hotels)
                
            else:
                error = 'Invalid login'
                return render_template('admin_login.html', error=error)
        else:
            error = 'User not found'
            return render_template('admin_login.html', error=error)
 
    return render_template('admin_login.html')

@app.route('/flights')
def flight_page():
    query="select * from Flights"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template('Flights.html',sqldata=data)

@app.route('/accomodation')
def accomodation_page():
    query="select * from Hotels"
    mycursor.execute(query)
    data=mycursor.fetchall()
    return render_template('Accomodation.html',sqldata=data)

@app.route('/accomodationbooking',methods=['GET','POST'])
def book_hotel():
    mycursor.execute('SELECT HotelID FROM Hotels')
    hotels =[row[0] for row in mycursor.fetchall()]
    if request.method == 'POST':
        user_email=request.form.get('email')
        hotel_name=request.form.get('hotel_id')
        date=request.form.get('date')

    
        query="insert into hotelBookings VALUES(%s,%s,%s,%s)"
        data=(str(num),user_email,hotel_name,date)
        mycursor.execute(query,data)
        mydb.commit()
        return render_template('Hotel_Booking.html')
    return render_template('Hotel_Booking.html',hotels=hotels)

@app.route('/flightbooking',methods=['GET','POST'])
def book_flight():
    mycursor.execute('SELECT FlightNumber FROM Flights')
    flights =[row[0] for row in mycursor.fetchall()]
    if request.method == 'POST':
        user_email=request.form.get('email')
        flight_name=request.form.get('flight_number')
        date=request.form.get('date')

    
        query="insert into flightBookings VALUES(%s,%s,%s,%s)"
        data=(str(num),user_email,flight_name,date)
        mycursor.execute(query,data)
        mydb.commit()
        return render_template('Flight_Booking.html')
    return render_template('Flight_Booking.html',flights=flights)


@app.route('/hotelbookings_visualization',methods=['POST','GET'])
def hotel_bookings_visualization():
#Assuming 'hotelBookings' table structure: BookingID, UserEmail, HotelID, Date
    mycursor.execute('SELECT HotelID, COUNT(*) AS BookingCount FROM hotelBookings GROUP BY HotelID') 
    data= mycursor.fetchall() #Create a DataFrame from the query result 
    df = pd.DataFrame(data, columns=['HotelID','BookingCount'])
    #Plotting 
    plt.bar(df['HotelID'],df['BookingCount'])
    plt.xlabel('HotelID') 
    plt.ylabel('Number of Bookings') 
    plt.title('HotelBookings Visualization') 
    plt.xticks(rotation=45)

    img = BytesIO() 
    plt.savefig(img,format='png')
    img.seek(0)
    plt.close() 
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('hotel_bookings_visualization.html', plot_url=plot_url) 

@app.route('/flightbookings_visualization')
def flight_bookings_visualization():
    mycursor.execute('SELECT FlightNumber, COUNT(*) AS BookingCount FROM flightBookings GROUP BY FlightNumber')
    data = mycursor.fetchall() #Create a DataFrame from the query result 
    df = pd.DataFrame(data, columns=['FlightNumber','BookingCount'])

    plt.bar(df['FlightNumber'],df['BookingCount'])
    plt.xlabel('FlightNumber') 
    plt.ylabel('Number of Bookings') 
    plt.title('Flight Bookings Visualization') 
    plt.xticks(rotation=45)
    img = BytesIO()
    plt.savefig(img,format='png')
    img.seek(0)
    plt.close() 
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('flight_bookings_visualization.html') 


 
@app.route('/deleteflight', methods=['GET','POST'])
def delete_flight():
    if request.method == 'POST':
        flight_number=request.form.get('flight_number')
    # Execute SQL DELETE query to delete the database record
    query = f'DELETE FROM Flights WHERE FlightNumber={flight_number}'
    mycursor.execute(query)
    mydb.commit()
 
    return redirect(url_for('admin'))
 

@app.route('/deletehotel', methods=['GET','POST'])
def delete_hotel():
    if request.method == 'POST':
        hotel_id=request.form.get('hotel_id')
    # Execute SQL DELETE query to delete the database record
    query = f'DELETE FROM Hotels WHERE HotelId={hotel_id}'
    mycursor.execute(query)
    mydb.commit()
 
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

    
