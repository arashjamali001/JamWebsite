from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.generic import DetailView,ListView
from .models import Project, Blog
import os


def health_check(request):
    """Simple health check endpoint"""
    try:
        # Get database configuration info
        from django.conf import settings
        db_info = {
            'engine': settings.DATABASES['default']['ENGINE'],
            'name': settings.DATABASES['default'].get('NAME', 'N/A'),
            'host': settings.DATABASES['default'].get('HOST', 'N/A'),
            'port': settings.DATABASES['default'].get('PORT', 'N/A'),
        }
        
        # Test database connection
        project_count = Project.objects.count()
        blog_count = Blog.objects.count()
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'database_info': db_info,
            'project_count': project_count,
            'blog_count': blog_count,
            'environment': os.environ.get('ENVIRONMENT', 'unknown'),
            'debug': settings.DEBUG
        })
    except Exception as e:
        import traceback
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'traceback': traceback.format_exc(),
            'environment': os.environ.get('ENVIRONMENT', 'unknown'),
            'database_url_set': bool(os.environ.get('DATABASE_URL'))
        }, status=500)


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.order_by('-id')[:4]
        context['blogs'] = Blog.objects.order_by('-id')[:4]
        return context

class AboutPageView(TemplateView):
    template_name = 'aboutme.html'


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        if blog.is_premium and not self.request.user.is_authenticated:
            context['locked'] = True
        return context

# "Show more" list views
class ProjectListView(ListView):
    model = Project
    template_name = 'project_list.html'
    context_object_name = 'projects'
    ordering = ['-id']
    paginate_by = 10 # Display 10 projects per page

class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-id']
    paginate_by = 15