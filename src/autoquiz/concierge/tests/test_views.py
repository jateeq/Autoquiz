from django.test import TestCase
from django.urls import reverse

from concierge.forms import MAX_DOCUMENT_CHARS


class IndexViewTests(TestCase):
    url = reverse("concierge:index")

    def test_get_renders_empty_form(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "concierge/index.html")
        self.assertFalse(response.context["form"].is_bound)

    def test_valid_post_renders_results(self):
        response = self.client.post(self.url, {"target_doc": "  Photosynthesis converts light.  "})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "concierge/results.html")
        self.assertEqual(response.context["results"], "Photosynthesis converts light.")

    def test_submitted_text_is_html_escaped(self):
        response = self.client.post(self.url, {"target_doc": "<script>alert(1)</script>"})

        self.assertNotContains(response, "<script>alert(1)</script>", html=False)
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")

    def test_blank_post_redisplays_form_with_error(self):
        response = self.client.post(self.url, {"target_doc": "   "})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "concierge/index.html")
        self.assertIn("target_doc", response.context["form"].errors)

    def test_oversized_post_is_rejected(self):
        response = self.client.post(self.url, {"target_doc": "a" * (MAX_DOCUMENT_CHARS + 1)})

        self.assertTemplateUsed(response, "concierge/index.html")
        self.assertIn("target_doc", response.context["form"].errors)

    def test_unsupported_method_is_rejected(self):
        response = self.client.put(self.url)

        self.assertEqual(response.status_code, 405)


class AboutViewTests(TestCase):
    def test_about_page_renders_and_marks_nav_active(self):
        response = self.client.get(reverse("concierge:about"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "concierge/about.html")
        self.assertContains(response, 'aria-current="page"', count=1)
