from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def limit_exceeded_view(request, limit_exception, template=None):
    if template is None:
        template = "django_limits/limit_exceeded.html"
    return render(
        request,
        template,
        {
            "exception": limit_exception,
            "model_name": limit_exception.model._meta.verbose_name,
            "model_name_plural": limit_exception.model._meta.verbose_name_plural
        },
        status=403
    )
