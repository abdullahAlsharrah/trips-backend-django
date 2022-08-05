def trips(trips):
    return [trip.id for trip in trips]
def username(profile):
    return str(profile.user.username)
    
def owner_image(profile):
    return str(f'http://127.0.0.1:8000/media/{profile.image}')