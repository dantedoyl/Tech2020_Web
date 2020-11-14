from app.models import Tag, Profile


def tags_n_users(request):
    return {
        'best_tags': Tag.objects.popular_tags(),
        'best_users': Profile.objects.popular_users()
    }
