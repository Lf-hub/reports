import datetime 
import pandas as pd
from core.models import Lines, File, Status, Company, Product, LogLineError


class Process():
    def __init__(self, file):
        self.file = file

    def main(self):
        # carrega o arquivo CSV
        df = pd.read_csv(self.file.file.name, sep=',')
        msg = ''
        # itera sobre as linhas do DataFrame
        list_not_in = []
        for index, row in df.iterrows():
            venda = row['venda']
            situacao = row['status']
            cliente = row['cliente']
            produto = row['produto']
            data_emissao = row['data_emissao']
            data_confirmacao = row['data_confirmacao']
            resultado = row['resultado']

            obj = Lines()
            
            obj.reference = venda
            obj.status = self.get_status(situacao)
            obj.client = self.get_client(cliente)
            obj.product = self.get_product(produto)
            obj.date_create = self.format_date(data_emissao) 
            obj.date_confirm = self.format_date(data_confirmacao)
            obj.profit = self.format_value(resultado)
            obj.transfer_fee_amount = '6'
            obj.result = self.process_result(obj.profit)

            if not Lines.objects.filter(reference=venda).exists():
                obj.save()
                list_not_in.append({'line':row['venda']})
                msg = "Lista Vendas incluidas"
            else:
                #list_not_in.append({'line':row['venda']})
                #msg = "Venda duplicada"
                pass
        
        LogLineError.objects.create(
            identifiy = msg,
            line = list_not_in
        )
    
    def get_status(self, param):
        status = Status.objects.get_or_create(name=param) 
        return status[0]
    
    def get_client(self, param):
        client = Company.objects.get_or_create(name=param)
        return client[0]
    
    def get_product(self, param):
        product = Product.objects.get_or_create(name=param)
        return product[0]
    
    def format_date(self, date_str):
        date = str(date_str).split('/')
        if len(date) == 2:
            date_str = str(date_str)+'/2023'
            date_format = datetime.datetime.strptime(str(date_str), "%d/%m/%Y").date()
        elif len(date) == 3:
            date_format = datetime.datetime.strptime(str(date_str), "%d/%m/%Y").date()
        else:
            date_format = None
        return date_format 

    def format_value(self, param):
        valor_str = param.replace('R$', '').strip()
        valor_str = valor_str.replace(' ', '')
        valor_str = valor_str.replace(',', '.')
        if valor_str.count('.') > 1:
            last_dot_position = valor_str.rfind('.')
            valor = float(valor_str[:last_dot_position].replace('.', '') + valor_str[last_dot_position:])
        else:
            valor = float(valor_str)
        return valor

    def process_result(self, param):
        res = param * 6 / 100
        return float(round(res,2))

    def compare(self):
        df = pd.read_csv(self.file.file.name, sep=',')
        list_not_in = []
        # itera sobre as linhas do DataFrame
        for index, row in df.iterrows():
            venda = row['venda']
            if not Lines.objects.filter(reference=venda):
                list_not_in.append(venda)
        teste = False
    
    def create_pdf(self):
        pass
