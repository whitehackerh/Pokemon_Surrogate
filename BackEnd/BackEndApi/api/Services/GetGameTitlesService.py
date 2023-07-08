from api.Enums.ResponseCodes import ResponseCodes
from api.Exceptions.CustomExceptions import CustomExceptions
from api.Services.BaseService import BaseService
from api.Models.GameTitles import GameTitles

class GetGameTitlesService(BaseService):
    def service(self):
        try:
            model = GameTitles()
            records = model.getGameTitles()
            data = self.__formatResponseData(records)
            return data
        except Exception as e:
            raise CustomExceptions(str(e), ResponseCodes.INTERNAL_SERVER_ERROR)
        
    def __formatResponseData(self, records):
        data = {'gameTitles': []}
        for record in records:
            data['gameTitles'].append({
                'id': record.id,
                'title': record.title
            })
        return data