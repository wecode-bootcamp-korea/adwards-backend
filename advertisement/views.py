import json
import bcrypt

from django.http            import HttpResponse, JsonResponse
from django.views           import View
from django.core.exceptions import ValidationError

from user.utils  import advertiser_login_required, user_login_required, advertiser_login_mark, user_login_mark
from user.models import User, Advertiser, InterestsType, State, Gender, UsersInterests
from .models     import (AdvertisementCategory,Tag,  AdvertisementTag, Advertisement,
                         AdvertisementLike, QuizHistory, AdvertisementsInterests 
                        )

class AdvertisementCreateListGetView(View):
    @advertiser_login_required 
    def post(self, request):
        data        = json.loads(request.body)
   
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
                    tag_id_list.append(tags.filter(name=tag)[0].id)
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

    @user_login_mark
    @advertiser_login_mark
    def get(self, request):        
        advertisements = Advertisement.objects 
    
        try:
            offset         = int(request.GET.get('offset', '0'))
            limit          = int(request.GET.get('limit', '3'))
            category_id    = int(request.GET.get('category_id','0'))
            price_per_view = request.GET.get('price_per_view', None)
            view           = request.GET.get('view', None)
            like           = request.GET.get('like', None)
            interests      = request.GET.get('interests', None)
            tag            = request.GET.get('tag', None)
            advertiser     = request.GET.get('advertiser', None)
            
            if advertiser == 'set':
                advertisements = advertisements.filter(advertiser=request.advertiser) 
                on_advertisements = advertisements.filter(switch=True)
                off_advertisements = advertisements.filter(switch=False)

                def querytolist(queryset):
                    result = [
                        {"advertisement_id": objects.id,
                        "title":             objects.title,
                        "thumbnail":         objects.thumbnail
                        } for objects in queryset
                    ] 
                    return result 

                return JsonResponse(
                        {"on_advertisement":querytolist(on_advertisements), 
                        "off_advertisement":querytolist(off_advertisements)}, 
                        status=200
                        )

            if category_id != 0:
                advertisements = advertisements.filter(ad_category_id=category_id)       
            
            if price_per_view == 'set': 
                advertisements = advertisements.order_by('-price_per_view')
 
            if like == 'set':
                advertisements = advertisements.order_by('-like_count')
            
            if view == 'set':
                advertisements = advertisements.order_by('-view_count')
            
            if tag: 
                tag = Tag.objects.filter(name=tag)[0]
                advertisements = advertisements.filter(tag = tag)
            
            if interests == 'set': 
                interests_list = request.user.interests.all()
                advertisements = (
                    list(set(advertisements.filter(interests__in=interests_list)))
                ) 

            if  not(advertiser or price_per_view or like or tag or view or interests): 
                advertisements = advertisements.order_by('-created_at')

            if type(advertisements) == list: 
                total_count = len(advertisements)
            else:
                total_count = advertisements.all().count()

            advertisements = advertisements[offset:limit]

            result = [
                {
                    "advertisement_id": advertisement.id,
                    "title":            advertisement.title,
                    "thumbnail":        advertisement.thumbnail,
                    "price_per_view":   advertisement.price_per_view,
                    "created_at":       advertisement.created_at
                } for advertisement in advertisements  
            ]

            return JsonResponse({"RESULT":result, "total_count":total_count}, status=200)
        
        except ValueError:
            return JsonResponse({"ERROR":"INVALID_QUERYSTRING"}, status=400)
        except AttributeError:
            return JsonResponse({"ERROR":"LOGIN_REQUIRED"}, status=401)
