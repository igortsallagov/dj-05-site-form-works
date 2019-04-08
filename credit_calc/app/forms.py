from django import forms


class CalcForm(forms.Form):
    initial_fee = forms.IntegerField(label="Стоимость товара")
    rate = forms.FloatField(label="Процентная ставка")
    months_count = forms.IntegerField(label="Срок кредита в месяцах")

    def clean_initial_fee(self):
        # валидация одного поля, функция начинающаяся на `clean_` + имя поля
        initial_fee = self.cleaned_data.get('initial_fee')
        if not initial_fee or initial_fee < 0:
            raise forms.ValidationError("Стоимость товара не может быть отрицательной или равной нулю")
        return initial_fee

    def clean(self):
        # общая функция валидации
        self.cleaned_data = super().clean()
        rate = self.cleaned_data.get('rate')
        months_count = self.cleaned_data.get('months_count')
        if rate and float(rate) < 0:
            self.add_error('rate', 'Процентная ставка не может быть отрицательной')
        if months_count and int(months_count) < 0:
            self.add_error('months_count', 'Срок кредита не может быть отрицательным')
        return self.cleaned_data
