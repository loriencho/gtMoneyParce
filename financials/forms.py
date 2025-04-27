from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    new_category = forms.CharField(required=False, max_length=20)

    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'category', 'date', 'new_category']

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().filter(user=user)
        self.fields['category'].required = False
        self.fields['new_category'].required = False

class EditTransactionForm(forms.ModelForm):
    new_category = forms.CharField(required=False, max_length=20)

    class Meta:
        model = Transaction
        fields = ['amount', 'type', 'category', 'date', 'new_category']

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, old, *args, **kwargs):
        super(EditTransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().filter(user=user)
        self.fields['category'].required = False
        self.fields['new_category'].required = False
        self.fields['amount'].initial = old.amount
        self.fields['date'].initial = old.date
        self.fields['type'].initial = old.type
        self.fields['category'].initial = old.category

class BudgetForm(forms.Form):
    budget = forms.DecimalField(decimal_places=2, max_digits=10)

class GraphTypeForm(forms.Form):
    btn = forms.CharField(initial='Totals')