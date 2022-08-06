from rest_framework.permissions import BasePermission

from trips.models import Question, Trip

class IsOwner(BasePermission):
    message = "You do not have permission to preform this action"
    
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsTripOwner(BasePermission):
    message = "You do not have permission to preform this action"
    
    def has_object_permission(self, request, view, obj):
        return obj.profile == request.user.profile

class isOwnerOfTrip(BasePermission):
    message = "You do not have permission to preform this action"
    
    def has_object_permission(self, request, view, obj):
        query = request.GET
        # question = Question.objects.get(id = int(query['question_id']))
        trip = Trip.objects.get(id=obj.trip)
        return trip.profile == request.user.profile