from django import forms
from blog.widgets import SearchInput

class SearchForm(forms.Form):
    keyword = forms.CharField(
        widget=SearchInput(placeholder="search keyword"))