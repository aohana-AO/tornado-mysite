from django import forms


class PostForm(forms.Form):
    title = forms.CharField(max_length=30, label='タイトル', widget=forms.Textarea(attrs={'cols': '100', 'rows': '2'}))
    content = forms.CharField(label='内容', widget=forms.Textarea(attrs={'cols': '140', 'rows': '6'}))

    address = forms.CharField(label='住所', widget=forms.Textarea(attrs={'cols': '100', 'rows': '1'}))
    latitude = forms.FloatField(label='緯度', widget=forms.Textarea(attrs={'cols': '100', 'rows': '1'}))
    longitude = forms.FloatField(label='内容', widget=forms.Textarea(attrs={'cols': '100', 'rows': '1'}))

    problemCategory = forms.fields.ChoiceField(

        choices=(
            ('環境問題', '環境問題'),
            ('いきもの', 'いきもの'),
            ('高齢者', '高齢者'),
            ('人間関係', '人間関係'),
            ('貧困', '貧困'),
            ('資源問題', '資源問題'),
            ('その他', 'その他')
        ),
        label='カテゴリー',
        required=True,
        widget=forms.widgets.Select
    )
    peopleNum = forms.fields.FloatField(

        label='内容', widget=forms.Textarea(attrs={'cols': '100', 'rows': '1'})
    )
    purpose = forms.fields.ChoiceField(

        choices=(
            ('議論したい', '議論したい'),
            ('相談したい', '相談したい'),
            ('行動したい', '行動したい'),
            ('その他', 'その他'),

        ),
        label='目的',
        required=True,
        widget=forms.widgets.Select
    )
    organization = forms.fields.ChoiceField(

        choices=(
            ('個人', '個人'),
            ('NPO・公共団体', 'NPO・公共団体'),
            ('地方自治体', '地方自治体'),
            ('一般企業', '一般企業'),
            ('その他', 'その他')
        ),
        label='搭載者種別',
        required=True,
        widget=forms.widgets.Select
    )
    problemSize = forms.fields.ChoiceField(

        choices=(
            ('小', '小'),
            ('中', '中'),
            ('大', '大'),
            ('その他', 'その他'),
        ),
        label='規模',
        required=True,
        widget=forms.widgets.Select
    )
    status = forms.fields.ChoiceField(

        choices=(
            ('募集中', '募集中'),
            ('募集終了（断念', '募集終了（断念）'),
            ('募集終了（解決）', '募集終了（解決）'),

        ),
        label='募集状態',
        required=True,
        widget=forms.widgets.Select
    )
