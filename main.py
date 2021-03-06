from flask import Flask, render_template, request, jsonify
from backend import trackQuery
from backend import environment
from backend import sp_search
from firebase_admin import credentials
import firebase_admin

app = Flask(__name__)


def start_firestore():

    # Disable app if happens to be enabled
    try:
        firebase_admin.delete_app(firebase_admin.get_app())
    except:
        pass

    try:
        firebase_admin.initialize_app()
    except:
        envData = environment.Data('dev')
        config = envData.config['pyrebaseConfig']
        localCredentials = credentials.Certificate(config['serviceAccount'])
        firebase_admin.initialize_app(localCredentials)

def stop_firestore():

    try:
        firebase_admin.delete_app(firebase_admin.get_app())
    except:
        pass

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/search')
def search():
  return render_template("search.html")

@app.route('/attribute_search', methods=['GET'])
def search_test(input = None, songInfo = None):
    start_firestore()

    if (input == None):
        input = {}
        for attribute in request.values.keys():
            input[attribute] = float(request.values[attribute])

    # TODO cleanup, ensure all incoming keys match the names in database

    if 'time_sig' in input:
        input['time_signature'] = input['time_sig']
        input.pop('time_sig', None)

    search = trackQuery.trackQuery()
    results = search.searchTracks(input, songInfo)

    stop_firestore()

    return jsonify(data=results)

@app.route('/track_search', methods=['GET'])
def search_by_track():

    input = {
        "track_name": request.values['track_name']
    }

    search = sp_search.sp_search()
    results_raw = search.track(input['track_name'])

    results = []

    for track in results_raw['tracks']['items']:

        json = {}
        json['name'] = track['name']
        json['artist_name'] = track['artists'][0]['name']
        json['album_name'] = track['album']['name']
        json['id'] = track['id']
        json['album_id'] = track['album']['id']
        json['album_art'] = track['album']['images'][0]['url']
        json['artist_id'] = track['artists'][0]['id']
        json['preview_url'] = track['preview_url']
        json['duration_ms'] = track['duration_ms']
        json['uri'] = track['uri']

        results.append(json)

    return jsonify(data=results)

@app.route('/id_search', methods=['GET'])
def search_for_id():
    track_id = request.values['track_id']
    #TODO check format of ID

    search = sp_search.sp_search()
    info = search.track_by_id(track_id)

    track_id = str(track_id)
    choices = search.audio_features(track_id)

    songInfo = {}
    songInfo['name'] = info[u'name']
    songInfo['artist_name'] = info[u'artists'][0][u'name']
    songInfo['album_name'] = info[u'album'][u'name']
    songInfo['id'] = info[u'id']
    songInfo['album_id'] = info[u'album'][u'id']
    songInfo['album_art'] = info[u'album'][u'images'][0][u'url']
    songInfo['artist_id'] = info[u'artists'][0][u'id']
    songInfo['preview_url'] = info[u'preview_url']
    songInfo['duration_ms'] = info[u'duration_ms']
    songInfo['uri'] = info[u'uri']

    choiceList = {}
    for attribute in choices[0]:
        if attribute == 'id' or attribute == 'type' or attribute == 'duration_ms' or attribute == 'uri' or attribute == 'analysis_url' or attribute == 'track_href':
            continue
        choiceList[attribute] = choices[0][attribute]

    results = search_test(choiceList, songInfo)

    return results


if __name__ == '__main__':
    #TODO turn this off?
    app.run(debug=False)
