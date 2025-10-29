from django import forms
from .models import AgentiComerciali, Contracte, Factura, FacturaItem, Plata, ContBancar


class AgentiComercialiForm(forms.ModelForm):
    class Meta:
        model = AgentiComerciali
        fields = "__all__"

class SupplierForm(forms.ModelForm):
    class Meta:
        model = AgentiComerciali
        fields = [
            "cod", "denumirea", "forma_juridica", "cod_fiscal",
            "denumirea_completa", "conducator", "adresa_juridica", 
            "adresa_postala", "telefoane", "rezident", "tara",
            "cod_tva", "cont_bancar_iban", "contract_baza", "email"
        ]
        widgets = {
            "cod": forms.TextInput(attrs={"class": "form-control"}),
            "denumirea": forms.TextInput(attrs={"class": "form-control"}),
            "forma_juridica": forms.TextInput(attrs={"class": "form-control"}),
            "cod_fiscal": forms.TextInput(attrs={"class": "form-control"}),
            "denumirea_completa": forms.TextInput(attrs={"class": "form-control"}),
            "conducator": forms.TextInput(attrs={"class": "form-control"}),
            "adresa_juridica": forms.TextInput(attrs={"class": "form-control"}),
            "adresa_postala": forms.TextInput(attrs={"class": "form-control"}),
            "telefoane": forms.TextInput(attrs={"class": "form-control"}),
            "tara": forms.TextInput(attrs={"class": "form-control"}),
            "cod_tva": forms.TextInput(attrs={"class": "form-control"}),
            "cont_bancar_iban": forms.TextInput(attrs={"class": "form-control"}),
            "contract_baza": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class ContracteForm(forms.ModelForm):
    class Meta:
        model = Contracte
        fields = "__all__"
        widgets = {
            "data_contractului": forms.DateInput(attrs={"type": "date"}),
            "termen_valabilitate": forms.DateInput(attrs={"type": "date"}),
            "data_indeplinirii_obligatiilor": forms.DateInput(attrs={"type": "date"}),
        }

class FacturaForm(forms.ModelForm):
    warnings = []

    class Meta:
        model = Factura
        fields = "__all__"
        widgets = {
            "data_facturii": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        contract = cleaned_data.get("contract")
        suma = cleaned_data.get("suma_facturii")
        budget_line = cleaned_data.get("budget_line")

        self.warnings = []

        if contract and suma:
            total = Factura.objects.filter(contract=contract).exclude(pk=self.instance.pk).aggregate(Sum('suma_facturii'))['suma_facturii__sum'] or 0
            remaining = contract.suma_contractului - total
            if suma > remaining:
                self.warnings.append(f"Atenție: suma facturii ({suma} MDL) depășește limita contractului. Rămâne doar {remaining} MDL.")

        if budget_line and suma:
            total_buget = Factura.objects.filter(budget_line=budget_line).exclude(pk=self.instance.pk).aggregate(Sum('suma_facturii'))['suma_facturii__sum'] or 0
            remaining_buget = budget_line.suma_alocata - total_buget
            if suma > remaining_buget:
                self.warnings.append(f"Atenție: suma facturii depășește bugetul pentru {budget_line.denumirea}. Rămâne doar {remaining_buget} MDL.")

        return cleaned_data




class FacturaItemForm(forms.ModelForm):
    class Meta:
        model = FacturaItem
        fields = "__all__"


class PlataForm(forms.ModelForm):
    class Meta:
        model = Plata
        fields = "__all__"
        widgets = {
            "data_platii": forms.DateInput(attrs={"type": "date"}),
        }

class ContBancarForm(forms.ModelForm):
    class Meta:
        model = ContBancar
        exclude = ['agent'] 
        fields = [
            "denumirea",
            "iban",
            "tip_cont",
            "prin_trezoreria",
            "decontari_directe",
            "valuta",
            "denumirea_trezoreriei",
            "cod_fiscal_trezorerie",
            "numar_cont_trezorerie",
            "banca_organizatiei",
            "banca_corespondent",
            "data_deschiderii",
            "data_inchiderii",
        ]
        widgets = {
            "data_deschiderii": forms.DateInput(attrs={"type": "date"}),
            "data_inchiderii": forms.DateInput(attrs={"type": "date"}),
        }

class ExcelUploadForm(forms.Form):
    file = forms.FileField(label="Importă fișier Excel")