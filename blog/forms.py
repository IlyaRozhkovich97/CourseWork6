from django.forms import ModelForm, BooleanField
from .models import Blog


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class BlogForm(StyleFormMixin):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'image', 'is_published']
