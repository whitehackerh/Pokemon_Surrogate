from django.db import models
from api.Enums.ResponseCodes import ResponseCodes
from api.Enums.RequestStatus import RequestStatus
from api.Exceptions.CustomExceptions import CustomExceptions
from django.db.models import Subquery, OuterRef
from api.Models.GameTitles import GameTitles
from api.Models.RequestPictures import RequestPictures

class Requests(models.Model):
    client_id = models.IntegerField()
    game_title_id = models.IntegerField()
    category = models.IntegerField()
    request_title = models.CharField(max_length=255)
    description = models.TextField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        app_label = 'api'
        db_table = 'requests'

    def getRequestsPersonalCount(self, client_id, statuses):
        try:
            return Requests.objects.filter(client_id=client_id, status__in=statuses).count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getRequestsPublicCount(self):
        try:
            return Requests.objects.filter(status=RequestStatus.ACCEPTING).count()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)

    def getRequestsPersonal(self, client_id, statuses, offset, limit):
        try:
            from api.models import Users
            return Requests.objects.filter(
                client_id=client_id,
                status__in=statuses
            ).annotate(
                smallest_sort_no=Subquery(
                    RequestPictures.objects.filter(
                        request_id=OuterRef('id'),
                        deleted_at__isnull=True
                    ).order_by('sort_no').values('sort_no')[:1]
                ),
                path=Subquery(
                    RequestPictures.objects.filter(
                        request_id=OuterRef('id'),
                        sort_no=OuterRef('smallest_sort_no'),
                        deleted_at__isnull=True
                    ).values('path')[:1]
                ),
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                nickname=Subquery(
                    Users.objects.filter(
                        id=client_id
                    ).values('nickname')[:1]
                )
            ).order_by('-id')[offset:offset+limit].all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
    
    def getRequestsPublic(self, offset, limit):
        try:
            return Requests.objects.filter(
                status=RequestStatus.ACCEPTING
            ).annotate(
                smallest_sort_no=Subquery(
                    RequestPictures.objects.filter(
                        request_id=OuterRef('id'),
                        deleted_at__isnull=True
                    ).order_by('sort_no').values('sort_no')[:1]
                ),
                path=Subquery(
                    RequestPictures.objects.filter(
                        request_id=OuterRef('id'),
                        sort_no=OuterRef('smallest_sort_no'),
                        deleted_at__isnull=True
                    ).values('path')[:1]
                ),
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
            ).order_by('-id')[offset:offset+limit].all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def getRequestDetail(self, request_id):
        try:
            from api.models import Users
            return Requests.objects.filter(
                id = request_id
            ).annotate(
                game_title=Subquery(
                    GameTitles.objects.filter(
                        id=OuterRef('game_title_id')
                    ).values('title')[:1]
                ),
                nickname=Subquery(
                    Users.objects.filter(
                        id=OuterRef('client_id')
                    ).values('nickname')[:1]
                ),
                clients_profile_picture=Subquery(
                    Users.objects.filter(
                        id=OuterRef('client_id')
                    ).values('profile_picture')[:1]
                )
            ).all()
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def updateRequest(self, request):
        try:
            requestRecord = Requests.objects.get(id=request.data.get('request_id'))
            requestRecord.game_title_id = request.data.get('game_title_id')
            requestRecord.category = request.data.get('category')
            requestRecord.request_title = request.data.get('request_title')
            requestRecord.description = request.data.get('description')
            requestRecord.min_price = request.data.get('min_price')
            requestRecord.max_price = request.data.get('max_price')
            requestRecord.save()
        except Exception as e:
            raise CustomExceptions(e, ResponseCodes.INTERNAL_SERVER_ERROR)
    
