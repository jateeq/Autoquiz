import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_http_methods

from .forms import TargetDocumentForm

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def index(request: HttpRequest) -> HttpResponse:
    """Accept a document and render the results page.

    The key-concept extraction step has not been implemented yet, so the results page
    currently echoes the submitted text back to the user.
    """
    if request.method == "POST":
        form = TargetDocumentForm(request.POST)
        if form.is_valid():
            target_doc = form.cleaned_data["target_doc"]
            logger.info("Received document of %d characters", len(target_doc))
            return render(request, "concierge/results.html", {"results": target_doc})
        logger.info("Rejected document submission: %s", form.errors.as_json())
    else:
        form = TargetDocumentForm()

    return render(request, "concierge/index.html", {"form": form})


@require_GET
def about(request: HttpRequest) -> HttpResponse:
    return render(request, "concierge/about.html")
