import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

# Clés d'API Spotify (remplacez-les par vos propres clés ou utilisez SpotifyOAuth pour une authentification utilisateur)
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"
REDIRECT_URI = "http://localhost:8888/callback"  # Lien de redirection après authentification

# Initialisation de l'authentification Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope='user-top-read')

# Création de l'objet Spotify
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Fonction pour récupérer les images d'albums depuis Spotify
def get_song_album_cover_url(track_name, artist_name):
    search_query = f"track:{track_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Image par défaut si aucune n'est trouvée

# Fonction de récupération des pistes actuelles de l'utilisateur sur Spotify
def get_current_top_tracks(limit=5, time_range='short_term'):
    try:
        top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)
        current_music_names = []
        current_music_posters = []

        for track in top_tracks['items']:
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            current_music_names.append(track_name)
            current_music_posters.append(get_song_album_cover_url(track_name, artist_name))

        return current_music_names, current_music_posters
    except spotipy.SpotifyException as e:
        st.error(f"Erreur Spotify : {str(e)}")
    except Exception as e:
        st.error(f"Erreur inattendue : {str(e)}")

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
        .song-name {
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

        st.subheader('Vos pistes actuelles sur Spotify')
        limit = st.slider('Nombre de pistes à afficher', min_value=1, max_value=10, value=5)
        time_range = st.selectbox('Période', ['short_term', 'medium_term', 'long_term'], index=0)

        if st.button('Afficher'):
            current_songs, current_posters = get_current_top_tracks(limit=limit, time_range=time_range)
            if current_songs and current_posters:
                st.subheader('Vos pistes actuelles:')
                for i, song in enumerate(current_songs):
                    st.markdown('<hr>', unsafe_allow_html=True)
                    st.markdown(f'<div class="recommended-song"><p class="song-name">{i+1}. {song}</p><img src="{current_posters[i]}" class="song-image"></div>', unsafe_allow_html=True)

    elif choice == 'À propos':
        st.header('À propos de cette application')
        st.write('Cette application utilise Streamlit pour créer une interface de recommandation musicale basée sur les pistes actuelles de l\'utilisateur sur Spotify.')

if __name__ == '__main__':
    main()
