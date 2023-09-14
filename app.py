from flask import Flask, request
from flask import render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import redirect
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dnevnik_spavanja.db'
db= SQLAlchemy()
db.init_app(app)


class San(db.Model):
        id_san= db.Column(db.Integer, primary_key=True)
        osoba= db.Column(db.Integer, nullable=False)
        dan = db.Column(db.Text)
        trajanje = db.Column(db.Integer)
        vrijeme_pocetka= db.Column(db.Text)
        vrijeme_zavrsetka= db.Column(db.Text)
        ocjena= db.Column(db.Integer)
        kvaliteta_sna= db.Column(db.Text)
        def __repr__(self):
               return '<san %r>'% self.id_san
class osoba(db.Model):
        id_osoba= db.Column(db.Integer,primary_key= True )
        korisnicko_ime= db.Column(db.Text,nullable=False)
        lozinka=db.Column(db.Text,nullable=False)
        dob=db.Column(db.Integer)
        potrebno_vrijeme_spavanja=db.Column(db.Integer)
        def __repr__(self):
               return '<osoba %r>'% self.id_osoba
         

        
        
@app.route('/',methods=["GET"])
def get_dreams():
    snovi=San.query.all()
    for san in snovi:
        hours = san.trajanje // 60
        minutes = san.trajanje % 60
        time_string = "{:0>2}:{:0>2}".format(hours, minutes)
        san.trajanje = time_string
        splited_string=san.dan.split("-")
        san.dan="{}.{}.{}.".format(splited_string[2],splited_string[1],splited_string[0])
    return render_template('dreams_list.html',snovi=snovi)


@app.route('/create-dream',methods=["GET","POST"])
def submit():
    if request.method == 'POST':
        san_content = request.form
        dream_start = san_content['dream_start']
        dream_finish = san_content['dream_finish']
    
        start_time = datetime.strptime(dream_start, '%H:%M')
        finish_time = datetime.strptime(dream_finish, '%H:%M')
        print (start_time)
        print (finish_time)
    
        time_difference = finish_time - start_time
        print(time_difference)
    
        total_minutes = time_difference.seconds // 60
        novi_san = San(osoba=1 , dan=san_content['dream_date'] , vrijeme_pocetka=san_content['dream_start'] , vrijeme_zavrsetka=san_content['dream_finish'] , ocjena=san_content['dream_quality'], kvaliteta_sna=san_content['dream_problems'],trajanje=total_minutes ) 
        # try:
        print(db.session)
        db.session.add(novi_san)
        db.session.commit()
        return redirect('/')
    else:
         return render_template('create-dream.html')


@app.route('/delete/<int:id>')
def delete(id):
    dream_to_delete = San.query.get_or_404(id)

    try:
        db.session.delete(dream_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Greška'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    san = San.query.get_or_404(id)
    print(san.kvaliteta_sna)
    if request.method == 'POST':
        san.ocjena= request.form['dream_quality']
        san.dan = request.form['dream_date']
        san.vrijeme_pocetka= request.form['dream_start']
        san.vrijeme_zavrsetka= request.form['dream_finish']
        san.kvaliteta_sna =request.form['dream_problems']
        dream_start = request.form['dream_start']
        dream_finish = request.form['dream_finish']
        start_time = datetime.strptime(dream_start, '%H:%M')
        finish_time = datetime.strptime(dream_finish, '%H:%M')
        print (start_time)
        print (finish_time)
   
        time_difference = finish_time - start_time
        print(time_difference)
   
        total_minutes = time_difference.seconds // 60
        san.trajanje = total_minutes
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Greška'

    else:
        return render_template('update.html', san=san)




      
if __name__ == "__main__":
        app.run(debug=True)