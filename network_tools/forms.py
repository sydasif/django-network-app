from django import forms


class PingForm(forms.Form):
    ip = forms.CharField(label="Host IP Address", required=True)
    port = forms.IntegerField(
        label="TCP Port", min_value=0, max_value=65535, required=True
    )


class CidrToNetmaskForm(forms.Form):
    cidr = forms.IntegerField(
        label="CIDR Value", min_value=1, max_value=32, required=True
    )


class NetmaskToCidrForm(forms.Form):
    netmask = forms.CharField(label="Netmask Value", required=True)


class CidrV6ToNetmaskForm(forms.Form):
    cidr_v6 = forms.IntegerField(
        label="CIDR Value", min_value=1, max_value=128, required=True
    )


class GetAllHostsForm(forms.Form):
    network_cidr = forms.CharField(label="Network CIDR", required=True)
