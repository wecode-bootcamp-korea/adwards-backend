import json
import bcrypt

from django.http            import HttpResponse, JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError
from django.db.utils        import IntegrityError

from user.utils  import advertiser_login_required, user_login_required
from user.models import User, Advertiser, InterestsType, State, Gender, UsersInterests
from .models     import (
    AdvertisementCategory,Tag,  
    AdvertisementTag,
    Advertisement,
    AdvertisementLike, 
    QuizHistory, 
    AdvertisementsInterests 
)

class AdvertisementView(View):
    @advertiser_login_required 
    def post(self, request):
        data = json.loads(request.body)
   
        try: 
            new_advertisement = ( 
                Advertisement.objects.create( 
                    advertiser_id  = request.user.id,
                    title          = data["title"],
                    description    = data["description"],
                    ad_category_id = data["ad_category_id"],
                    video_link     = data["video_link"],
                    thumbnail      = data["thumbnail"],
                    budget         = data["budget"],
                    price_per_view = data["price_per_view"],
                )
            )
            
            interests_bulk = [
                    AdvertisementsInterests(
                        advertisement_id  = new_advertisement.id,
                        interests_type_id = interests
                    ) for interests in data["interests_type_id"] 
            ]     
            AdvertisementsInterests.objects.bulk_create(interests_bulk) 

            tag_list    = data["tag"]
            tag_id_list = []
            tags        = Tag.objects

            for tag in tag_list: 
                if tags.filter(name=tag).exists():
                    tag_id_list.append(tags.get(name=tag).id)
                else:
                    new_tag = tags.create(name=tag)
                    tag_id_list.append(new_tag.id) 
            
            tag_bulk = [
                AdvertisementTag(
                    advertisement_id = new_advertisement.id,
                    tag_id           = tag_id
                ) for tag_id in tag_id_list
            ]
            AdvertisementTag.objects.bulk_create(tag_bulk)
            
            return JsonResponse({"advertisement_id":new_advertisement.id}, status=200)
    
        except KeyError:
            return JsonResponse({"ERROR":"KEY_MISSING"}, status=400)
        except ValidationError:
            return JsonResponse({"ERROR":"STRING_IN_NUMBER"}, status=400)

class UserAdvertisementsView(View):
    @user_login_required
    def get(self, request):
        try:
            offset = int(request.GET.get('offset', '0'))
            limit  = int(request.GET.get('limit', '3'))

        except ValueError:
            return JsonResponse({"ERROR":"INVALID_QUERYSTRING"}, status=400)

        interests_list = request.user.interests.all()
        advertisements = (
            Advertisement.objects.filter(
                deleted=False, switch=True, interests__in=interests_list 
                ).distinct()
        ) 

        total_count = advertisements.count()
        advertisements = advertisements[offset:limit]    
        
        result = [
            {
                "advertisement_id": advertisement.id,
                "title":            advertisement.title,
                "thumbnail":        advertisement.thumbnail,
                "price_per_view":   int(advertisement.price_per_view),
            } for advertisement in advertisements  
        ]
        return JsonResponse({"RESULT":result, "total_count":total_count}, status=200)

    def post(self, request):
        try:  
            offset = int(request.GET.get("offset", "0"))
            limit  = int(request.GET.get("limit", "3"))
            data   = json.loads(request.body)
            tag    = request.GET.get("tag", None)
            category_id = (
                int(request.GET["category_id"]) if "category_id" in request.GET  else None
                ) 

        except ValueError:
            return JsonResponse({"ERROR":"INVALID_QUERYSTRING"}, status=400)

        try:
            advertisements = Advertisement.objects.filter(deleted=False, switch=True)       

            if Tag.objects.filter(name=tag).exists(): 
                advertisements = advertisements.filter(tag=Tag.objects.get(name=tag))
            
            if category_id:
                advertisements = advertisements.filter(ad_category_id=category_id)       

            if 'order_by' in data:
                for order in data['order_by']:
                    field = order['field']
                    asc = '-' if not order['asc'] else ""  
                    advertisements = advertisements.order_by(f"{asc}{field}")
            
            total_count = advertisements.count() 
            advertisements = advertisements[offset:limit]
            
            result = [
                {
                    "advertisement_id": advertisement.id,
                    "title":            advertisement.title,
                    "thumbnail":        advertisement.thumbnail,
                    "price_per_view":   int(advertisement.price_per_view),
                } for advertisement in advertisements  
            ]

            return JsonResponse({"RESULT":result, "total_count":total_count}, status=200)
        except Exception as e: 
            return JsonResponse({"ERROR":f"{e}"})
        
class AdvertiserAdvertisementsView(View):
    @advertiser_login_required
    def get(self, request):
        advertisements = Advertisement.objects.filter(deleted=False, advertiser=request.user)
        on_advertisements  = advertisements.filter(switch=True)
        off_advertisements = advertisements.filter(switch=False)

        def querytolist(queryset):
            result = [
                {"advertisement_id": objects.id,
                "title":             objects.title,
                "thumbnail":         objects.thumbnail
                } for objects in queryset
            ] 
            return result 

        return JsonResponse({
            "on_advertisement":querytolist(on_advertisements), 
            "off_advertisement":querytolist(off_advertisements)
            }, status=200
        )

class AdvertiserAdvertisementDetailView(View):
    @advertiser_login_required
    def get(self, request, advertisement_id):
        try:
            advertisement = Advertisement.objects.filter(deleted=False).get(id=advertisement_id) 
            advertiser = request.user

            tags = advertisement.tag.all()
            tag_list = [tag.name for tag in tags]

            interests = advertisement.interests.all()
            interests_type_id_list = [interest.id for interest in interests]

            result = {
              "title":             advertisement.title,
              "description":       advertisement.description,
              "video_link":        advertisement.video_link,
              "view_count":        advertisement.view_count,
              "price_per_view":    int(advertisement.price_per_view),
              "advertiser_id":     advertisement.id,
              "tag":               tag_list,
              "thumbnail":         advertisement.thumbnail,
              "budget":            int(advertisement.budget),
              "interests_type_id": interests_type_id_list,
              "switch":            advertisement.switch
            }

            return JsonResponse({"RESULT": result}, status=200)

        except Advertisement.DoesNotExist:
            return JsonResponse({"ERROR":"INVALID_ADVERTISEMENT_ID"}, status=404)
    
    @advertiser_login_required
    def delete(self, request, advertisement_id):
        try:
            advertisement = Advertisement.objects.filter(deleted=False).get(id=advertisement_id)
            advertisement.deleted = True
            advertisement.save() 

            return HttpResponse(status=200)  
        
        except Advertisement.DoesNotExist:
            JsonResoponse({"ERROR":"INVALID_ADVERTISEMENT_ID"}, status=404)
    
    @advertiser_login_required
    def post(self, request, advertisement_id):
        data = json.loads(request.body)
        try:
            advertisement = Advertisement.objects.filter(deleted=False).get(id=advertisement_id)
           
            if "title" in data:
                advertisement.title = data["title"]

            if "description" in data:
                advertisement.description = data["description"]

            if "ad_category_id" in data:
                advertisement.ad_category_id = data["ad_category_id"] 

            if "video_link" in data: 
                advertisement.video_link =data["video_link"]

            if "thumbnail" in data: 
                advertisement.thumbnail = data["thumbnail"]
            
            if "budget" in data:
                advertisement.budget = data["budget"]

            if "switch" in data: 
                advertisement.switch = data["switch"]

            if "interests_type_id" in data: 
                interests = InterestsType.objects.filter(id__in=data["interests_type_id"])
                advertisement.interests.set(interests)

            if "tag" in data: 
                tag_updated = data["tag"]
                tag_list    = []
                tags        = Tag.objects

                for tag in tag_updated: 
                    if tags.filter(name=tag).exists():
                        tag_list.append(tags.get(name=tag))
                    else:
                        new_tag = tags.create(name=tag)
                        tag_list.append(new_tag) 

                advertisement.tag.set(tag_list) 
     
            advertisement.save()

            return HttpResponse(status=200)

        except Advertisement.DoesNotExist:
            return JsonResoponse({"ERROR":"INVALID_ADVERTISEMENT_ID"}, status=404)
        except ValidationError:
            return JsonResoponse({"ERROR":"INVALID_DATA_TYPE"})
        except IntegrityError:
            return JsonResoponse({"ERROR":"INVALID_INPUT"})

class UserAdvertisementDetailView(View):
    def get(self,request, advertisement_id):
        try: 
            advertisement = Advertisement.objects.filter(deleted=False, switch=True).get(id=advertisement_id)

            tags = advertisement.tag.all()
            tag_list = [tag.name for tag in tags]

            result = {
              "title":             advertisement.title,
              "description":       advertisement.description,
              "video_link":        advertisement.video_link,
              "view_count":        advertisement.view_count,
              "price_per_view":    int(advertisement.price_per_view),
              "advertiser_id":     advertisement.id,
              "company_name":      advertisement.advertiser.company_name,
              "tag":               tag_list,
              "thumbnail":         advertisement.thumbnail,
            }

            return JsonResponse({"RESULT": result}, status=200)

        except Advertisement.DoesNotExist:
            return JsonResponse({"ERROR":"INVALID_ADVERTISEMENT_ID"}, status=404)
