from .models import SiteSettings

def site_settings(request):
    obj = SiteSettings.objects.filter(is_active=True).first()
    return {'site_settings': obj}
