from django.db import models

# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to='media/relatorios/')
    date_create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file.name


class Status(models.Model):
    name = models.CharField(max_length=60, verbose_name=('nome'))
    slug = models.SlugField(max_length=16, verbose_name=('slug'))

    class Meta:
        verbose_name = ('Situação')
        verbose_name_plural = ('Situações')

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=60, verbose_name=('nome'))
    doc_number = models.CharField(max_length=60, verbose_name=('CNPJ'), blank=True, null=True)
    slug = models.SlugField(max_length=16, verbose_name=('slug'), blank=True, null=True)

    class Meta:
        verbose_name = ('Cliente')
        verbose_name_plural = ('Clientes')

    def __str__(self):
        return self.name     


class Product(models.Model):
    name = models.CharField(max_length=60, verbose_name=('nome'))
    slug = models.SlugField(max_length=16, verbose_name=('slug'), blank=True, null=True)

    class Meta:
        verbose_name = ('Produto')
        verbose_name_plural = ('Produtos')

    def __str__(self):
        return self.name


class Lines(models.Model):
    file = models.ForeignKey(File, verbose_name=('Arquivo'),  on_delete=models.CASCADE, blank=True, null=True )
    reference = models.IntegerField(("codigo da venda"))
    status = models.ForeignKey(Status, verbose_name=('Situação'),  on_delete=models.CASCADE, blank=True, null=True )
    client = models.ForeignKey(Company, verbose_name=('Cliente'),  on_delete=models.CASCADE, blank=True, null=True )
    product = models.ForeignKey(Product, verbose_name=('Produto'),  on_delete=models.CASCADE, blank=True, null=True )
    date_create = models.DateField(verbose_name=("Data da Emissão"), blank=True, null=True)
    date_confirm = models.DateField(verbose_name=("Data da Comfirmação"), blank=True, null=True)
    profit = models.FloatField(default=0, verbose_name=('Lucro empresa'), blank=True, null=True)
    transfer_fee_amount = models.CharField(max_length=128, blank=True, null=True, verbose_name=('Valor da Taxa'))
    result = models.FloatField(default=0, verbose_name=('Lucro Líquido'), blank=True, null=True)

    class Meta:
        verbose_name = ('Venda')
        verbose_name_plural = ('Vendas')

    def __str__(self):
        return str(self.reference)

class LogLineError(models.Model):
    reference = models.IntegerField(("Referencia"),blank=True, null=True,)
    identifiy = models.CharField(max_length=100, blank=True, null=True, verbose_name='Erro')
    line = models.JSONField(blank=True, null=True, verbose_name=('Linha'))

    class Meta:
        verbose_name = ('Erros')
        verbose_name_plural = ('Erros')

    def __str__(self):
        return str(self.reference)