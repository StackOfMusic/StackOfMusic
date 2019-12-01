from django import forms
from music.models import Comment


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment_text',
        )

    def __init__(self, user, music, *args, **kwargs):
        self.user = user
        self.music = music
        super(CreateCommentForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance.user = self.user
        self.instance.music = self.music
        return super(CreateCommentForm, self).save(commit=commit)
