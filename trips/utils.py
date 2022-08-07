from trips.models import Question


def trips(trips):
    return [trip.id for trip in trips]

def username(profile):
    return str(profile.user.username)
    
def owner_image(profile):
    return str(f'http://10.0.2.2:8000/media/{profile.image}')