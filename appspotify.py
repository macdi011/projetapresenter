import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Clés d'API Spotify (remplacez-les par vos propres clés)
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialisation du client Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Chargement des données à partir du fichier CSV avec spécification de l'encodage
try:
    music = pd.read_csv('spotify-2023.csv', encoding='utf-8')  # Assurez-vous que le chemin est correct et spécifiez l'encodage approprié
except UnicodeDecodeError:
    st.error("Erreur de décodage Unicode lors de la lecture du fichier CSV.")

# Fonction pour récupérer les images d'albums depuis Spotify
def get_song_album_cover_url(track_name, artists_name):
    search_query = f"track:{track_name} artist:{artists_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Image par défaut si aucune n'est trouvée

# Fonction de recommandation basée sur le clustering
def recommend(song, music):
    try:
        index = music[music['track_name'] == song].index[0]
        recommended_music_titles = []
        recommended_music_posters = []
        
        # Logique de recommandation
        for i in range(index + 1, min(index + 6, len(music))):  
            artists = music.iloc[i]['artist(s)_name']  # Nom des artistes
            recommended_music_posters.append(get_song_album_cover_url(music.iloc[i]['track_name'], artists))
            recommended_music_titles.append(music.iloc[i]['track_name'])

        return recommended_music_titles, recommended_music_posters
    except IndexError:
        st.error(f"Aucune chanson trouvée avec le titre '{song}'. Veuillez essayer avec un autre titre de chanson.")
    except KeyError:
        st.error(f"Erreur de clé lors de la recherche de '{song}' dans les données musicales.")

# Fonction principale pour l'application Streamlit
def main():
    st.title('Application de Recommandation Musicale')
    st.markdown(
        """
        <style>
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #FF5733;
            text-align: center;
            margin-bottom: 20px;
        }
        .input-container {
            margin-bottom: 20px;
        }
        .recommended-song {
            margin-top: 30px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .song-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .song-image {
            width: 200px;
            height: auto;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Menu de navigation
    menu = ['Accueil', 'À propos']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'Accueil':
        st.markdown('<hr>', unsafe_allow_html=True)
        st.header('Accueil')

        # Formulaire pour saisir un titre de chanson
        st.subheader('Recherche de chanson')
        song_name = st.text_input('Titre de la chanson')

        if st.button('Rechercher'):
            if song_name:
                recommended_songs, recommended_posters = recommend(song_name, music)
                if recommended_songs and recommended_posters:
                    st.subheader('Chansons Recommandées:')
                    
                    # Affichage des chansons recommandées avec leurs images d'album
                    for i, title in enumerate(recommended_songs):
                        st.markdown('<hr>', unsafe_allow_html=True)
                        st.markdown(f'<div class="recommended-song"><p class="song-title">{i+1}. {title}</p><img src="{recommended_posters[i]}" class="song-image"></div>', unsafe_allow_html=True)

    elif choice == 'À propos':
        st.header('À propos de cette application')
        st.write('Cette application utilise Streamlit pour créer une interface de recommandation musicale basée sur le clustering. Elle se connecte à Spotify pour récupérer les images des albums.')

if __name__ == '__main__':
    main()
