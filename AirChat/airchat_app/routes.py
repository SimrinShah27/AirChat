import os
import sys
sys.path.append(os.path.abspath('../airchat'))

from airchat import *
import requests,json
from flask import render_template,request,jsonify
import difflib
from datetime import datetime
from sqlalchemy import text



@app.route('/')
def chatbot():  
    return render_template('chatbot.html')

#Api call for the cheapest flight
def cheapestFlight(payload): 
    try:
        querystring = payload
        querystring['depart_date'] = querystring['depart_date'].replace('/','-')
        querystring['return_date'] = querystring['return_date'].replace('/','-')
        querystring['page'] = "None"
        querystring['currency'] = "USD"

        dest=querystring['destination']

        response = requests.request("GET", cheapPriceUrl, headers=headers, params=querystring)
        info = json.loads(response.text)
        details=[]
        if info['data'] == {}:
            return jsonify([{'Alert':'Could not find flights for this date!!'}])

        else:
            dataset=info['data'][dest]


            if info['success']=='True' or info['success']:
                for key,val in dataset.items():
                    k={}
                    airline = dataset[key]['airline']
                    if airline != '':
                        try:
                            x=Airlines.query.filter_by(airline_iata=airline).first()
                            k['Airline Name']=x.airline_name
                        except:
                            k['Airline Name']='Private Airline'
                    k['Flight No']=dataset[key]['flight_number']
                    depart_details=(dataset[key]['departure_at']).split('T')
                    k['Departure Details']=datetime.strftime(datetime.strptime(depart_details[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +depart_details[1].split('-')[0]
                    return_details=(dataset[key]['return_at']).split('T')
                    k['Return Details']=datetime.strftime(datetime.strptime(return_details[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +return_details[1].split('-')[0]
                    k['Price']=str(dataset[key]['price'])+" USD"

                    details.append(k)



            return jsonify(details)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method cheapestFlight: ", str(e), "at line number: ",str(exc_tb.tb_lineno))


#Api call for the cheapest flight grouped by month
def cheapestFlightGroupedByMonth(payload):

    try:
        querydata = payload
        querydata['currency'] = "USD"
        querydata['length'] = "3"

        response = requests.request("GET", cheapPriceMonthUrl, headers=headers, params=querydata)
        infodata = json.loads(response.text)
        detailsdata=[]
        datasetmonth=infodata['data']

        if infodata['success']=='True' or infodata['success']:
            for key,val in datasetmonth.items():
                kdata={}
                kdata['Month'] = key
                airline = datasetmonth[key]['airline']
                if airline != '':
                    try:
                        x=Airlines.query.filter_by(airline_iata=airline).first()
                        kdata['Airline Name']=x.airline_name
                    except:
                        kdata['Airline Name']='Private Airline'
                kdata['Flight No']=datasetmonth[key]['flight_number']
                depart_details=(datasetmonth[key]['departure_at']).split('T')
                kdata['Departure Details']=datetime.strftime(datetime.strptime(depart_details[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +depart_details[1].split('-')[0]
                return_details=(datasetmonth[key]['return_at']).split('T')
                kdata['Return Details']=datetime.strftime(datetime.strptime(return_details[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +return_details[1].split('-')[0]
                kdata['Price']=str(datasetmonth[key]['price'])+" USD"
                kdata['Transfers'] = datasetmonth[key]['transfers']

                detailsdata.append(kdata)

        return jsonify(detailsdata)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method cheapestFlightGroupedByMonth: ", str(e), "at line number: ",str(exc_tb.tb_lineno))


#Api call for the prices to the nearest to the cities mentioned
def pricesForAlternateDirections(payload):
    try:
        querystring = payload
        querystring['currency'] = "USD"
        querystring['flexibility'] = "0"
        querystring['show_to_affiliates'] = "true"
        querystring['limit'] = "10"
        querystring['distance'] = "100"
        origin = querystring['origin']


        response = requests.request("GET", nearestPlacesMatrixUrl, headers=headers, params=querystring)
        infodata = json.loads(response.text)
        detailsdata=[]
        dataset = infodata['prices']
        

        if dataset != []:
            for item in dataset:
                kdata={}
                if origin != item['origin']:
                    airline = item['main_airline']
                    if airline != '':
                        try:
                            x=Airlines.query.filter_by(airline_iata=airline).first()
                            kdata['Airline Name']=x.airline_name
                        except:
                            kdata['Airline Name']='Private Airline'

                    alt_origin=item['origin']
                    if alt_origin != '':
                        try:
                            x=Airports.query.filter_by(airport_iata=alt_origin).first()
                            kdata['Origin']=x.airport_name
                            kdata['City']=x.city
                        except:
                            kdata['Origin']=alt_origin
                            kdata['City']=alt_origin


                    kdata['Destination']=item['destination']
                    depart_details=(item['depart_date']).split('T')
                    kdata['Departure Details']=datetime.strftime(datetime.strptime(depart_details[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +depart_details[1].split('-')[0]
                    kdata['Price']=str(item['price'])+" USD"
                    kdata['Transfers'] = item['transfers']
                    kdata['Duration in mins'] = item['duration']
                    
                    detailsdata.append(kdata)

        return jsonify(detailsdata)
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method pricesForAlternateDirections: ", str(e), "at line number: ",str(exc_tb.tb_lineno))


#Api call for the real-time flight data
def realTimeFlightDetails(payload):  
    try:
        querystring = payload
        querystring['limit'] = 1
        headers = {}

        response = requests.request("GET", realTimeFlightUrl, headers=headers, params=querystring)
        info = json.loads(response.text)
        details = []
        dataset = info['data']
        for item in dataset:
            k={}

            k['Flight Date']=item['flight_date']
            k['Flight Status']=item['flight_status']
            k['Departure Airport']=item['departure']['airport']
            k['Departure Timezone']=item['departure']['timezone']
            k['Departure Terminal']=item['departure']['terminal']
            k['Departure Gate']=item['departure']['gate']
            scheduled_time=(item['departure']['scheduled']).split('T')
            k['Departure Scheduled']=datetime.strftime(datetime.strptime(scheduled_time[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +scheduled_time[1].split('+')[0]
            estimated_time=(item['departure']['estimated']).split('T')
            k['Departure Estimated']=datetime.strftime(datetime.strptime(estimated_time[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +estimated_time[1].split('+')[0]

            k['Arrival Airport']=item['arrival']['airport']
            k['Arrival Timezone']=item['arrival']['timezone']
            k['Arrival Terminal']=item['arrival']['terminal']
            k['Arrival Gate']=item['arrival']['gate']
            k['Arrival Baggage']=item['arrival']['baggage']
            arr_scheduled_time=(item['arrival']['scheduled']).split('T')
            k['Arrival Scheduled']=datetime.strftime(datetime.strptime(arr_scheduled_time[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +arr_scheduled_time[1].split('+')[0]
            arr_estimated_time=(item['arrival']['estimated']).split('T')
            k['Arrival Estimated']=datetime.strftime(datetime.strptime(arr_estimated_time[0], "%Y-%m-%d"), "%Y/%m/%d") + " " +arr_estimated_time[1].split('+')[0]

            k['Airline Name']=item['airline']['name']
            
            details.append(k)

        return jsonify(details)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method realTimeFlightDetails: ", str(e), "at line number: ",str(exc_tb.tb_lineno))

#Ratings

def tweetsRatings(payload):  
    try:
        airlineName, category = payload['airlineName'],payload['category']
        sql = text("SELECT airline_sentiment,airline_sentiment_conf,airline,text FROM Ratings")
        rows = db.engine.execute(sql)
        headers = ["airline_sentiment", "airline_sentiment_confidence","airline","text"]

        data = {}
        for i in headers:
            data[i] = []
        for i in rows:
            for j in range(len(i)):
                data[headers[j]].append(i[j])

        book_ct = []
        lugg_ct = []
        for i in range(len(data['text'])):
            if "book" in data['text'][i] or "reserv" in data['text'][i] or "appoint" in data['text'][i] or "web" in \
                    data['text'][i]:
                book_ct.append(i)
            if "bag" in data['text'][i] or "luggage" in data['text'][i] or "suit" in data['text'][i] or "kit" in \
                    data['text'][i] or "belonging" in data['text'][i] or "goods" in data['text'][i] or "trunk" in \
                    data['text'][i]:
                lugg_ct.append(i)

        airlines = list(set(data['airline']))

        ratings = {'negative': 1, 'positive': 5, 'neutral': 3}
        book_airlines = {}
        if category == 'a':
            for i in airlines:
                book_airlines[i] = []
            for i in book_ct:
                book_airlines[data['airline'][i]].append(
                    ratings[data["airline_sentiment"][i]] * data["airline_sentiment_confidence"][i])
            overallRating=str(round(sum(book_airlines[airlineName]) / len(book_airlines[airlineName]),2))+' / 5  '
        elif category == 'b':
            lugg_airlines = {}
            for i in airlines:
                lugg_airlines[i] = []
            for i in lugg_ct:
                lugg_airlines[data['airline'][i]].append(
                    ratings[data["airline_sentiment"][i]] * data["airline_sentiment_confidence"][i])
            overallRating=str(round(sum(lugg_airlines[airlineName]) / len(lugg_airlines[airlineName]),2))+' / 5  '
        else:
            rating_airlines = {}
            for i in airlines:
                rating_airlines[i] = []
            for i in range(len(data['airline'])):
                rating_airlines[data['airline'][i]].append(
                    ratings[data["airline_sentiment"][i]] * data["airline_sentiment_confidence"][i])
            overallRating = str(round(sum(rating_airlines[airlineName]) / len(rating_airlines[airlineName]),2))+' / 5  '
        toReturn=[{'Rating': overallRating}]
        return jsonify(toReturn)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method validate_code: ", str(e), "at line number: ",str(exc_tb.tb_lineno))

@app.route('/validate_code',methods=['POST'])
def validate_code():
    try:
        data=request.form['msg']
        print(data)
        if len(data) == 3:
            data1=data.upper()
            x=Airports.query.filter_by(airport_iata=data1).first()
            if x is not None:
                toReturn={"return": '1','airport_name':x.airport_name,'city':x.city,'airport_iata':x.airport_iata}
            else:
                toReturn={"return": '0','airport_name':'','city':''}
        else:
            airport=Airports.query.all()
            airport_city=[air.city for air in airport]
            best_match = difflib.get_close_matches(data,airport_city,1)
            if best_match == []:
                toReturn={"return": '0','airport_name':'','city':''}
            else:
                best_match=best_match[0]
                x=Airports.query.filter_by(city=best_match).first()
                toReturn={"return": '1', 'airport_name':x.airport_name,'city':x.city,'airport_iata':x.airport_iata}

        return jsonify(toReturn)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method validate_code: ", str(e), "at line number: ",str(exc_tb.tb_lineno))

@app.route('/send_email',methods=['POST'])
def send_email():
    try:
        email=request.form['email']
        body = json.loads(request.form['payload'])
        rabbitmqsend.add_queue(email,body['body'])
        return jsonify({'status':'success'})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method send_email: ", str(e), "at line number: ",str(exc_tb.tb_lineno))





def get_intent(message):
    try:
        intent_var=''
        print("Message: ",message)
        x=Intent.query.all()
        for intent in x:
            str_list=json.loads(intent.training_data)
            best_match = difflib.get_close_matches(message,str_list)
            if best_match != []:
                intent_var=intent.intent_name
                value = Intent.query.filter_by(intent_name=intent_var).first()
                score = int((difflib.SequenceMatcher(None, message, best_match[0]).ratio())*100)
                print(score)
                if intent.score == 0:
                    score_new = score
                else:
                    score_new = int((intent.score + score)/2)
                print(score_new)
                value.score = score_new
                db.session.commit()
            else:
                best_match=[]
        print("best_match:",intent_var)

        if intent_var == '':
            return None
        else:
            return intent_var

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method get_intent: ", str(e), "at line number: ",str(exc_tb.tb_lineno))



def build_response(identified_intent_name, payload):
    try:
        response = ''
        if identified_intent_name == 'cheap tickets':
            response = cheapestFlight(payload)
        elif identified_intent_name == 'cheap tickets by month':
            print(identified_intent_name)
            response = cheapestFlightGroupedByMonth(payload)
        elif identified_intent_name == 'alternate directions':
            response = pricesForAlternateDirections(payload)
        elif identified_intent_name == 'track flight':
            response = realTimeFlightDetails(payload)
        elif identified_intent_name == 'ratings':
            response = tweetsRatings(payload)
        else:
            response = jsonify([{'Alert':'Sorry unable to understand!!'}])
        
        return response
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method build_response: ", str(e), "at line number: ",str(exc_tb.tb_lineno))




@app.route('/execute_query',methods=['POST'])
def execute_query():
    # Get and Set User details
    try:
        message = request.form['message']
        payload = json.loads(request.form['payload'])
        print("payload: ",payload)

        identified_intent_name = get_intent(message)
        if identified_intent_name is not None:
            intent_identified_flag=1
        else:
            intent_identified_flag=0
        print("identified_intent_name: ",identified_intent_name)
        if identified_intent_name is None:
            identified_intent_name=''
        if 'params' in payload:
            if payload['params']=='0':
                msg_rec=MessageHistory(message_received=message,bot_response='',intent_name=identified_intent_name,intent_identified_flag=intent_identified_flag)
                db.session.add(msg_rec)
                db.session.commit()
                return jsonify({'intent':identified_intent_name})
        response = build_response(identified_intent_name, payload)

        msg_rec=MessageHistory(message_received=message,bot_response=str(response),intent_name=identified_intent_name,intent_identified_flag=intent_identified_flag)
        db.session.add(msg_rec)
        db.session.commit()

        return response

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("Error in method execute: ", str(e), "at line number: ",str(exc_tb.tb_lineno))
