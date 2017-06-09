# -*- coding: utf-8 -*-
"""
    pyboleto.bank.santander
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lógica para boletos do banco Santander.
    Carteira ``'101'`` Com Registro
    Carteira ``'102'`` Sem Registro
    Carteira ``'201'`` Penhor Rápido Com Registro

    Baseado no projeto `BoletoPHP <http://boletophp.com.br/>`

    :copyright: © 2011 - 2012 by Eduardo Cereto Carvalho
    :license: BSD, see LICENSE for more details.

"""
from pyboleto.data import BoletoData, CustomProperty
from pyboleto.pdf import BoletoFields


class BoletoSantander(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco Santander
    '''

    nosso_numero = CustomProperty('nosso_numero', 12)

    #: Também chamado de "ponto de venda"
    agencia_cedente = CustomProperty('agencia_cedente', 4)

    #: Também chamdo de código do cedente, se for uma conta de 9 dígitos
    #: ignorar os 2 primeiros
    conta_cedente = CustomProperty('conta_cedente', 7)

    def __init__(self, **kwargs):
        super(BoletoSantander, self).__init__(**kwargs)

        self.codigo_banco = "033"
        self.logo_image = "logo_santander.jpg"
        self.carteira = '102'
        # IOS - somente para Seguradoras (Se 7% informar 7, limitado 9%)
        # Demais clientes usar 0 (zero)
        self.ios = "0"

    def format_nosso_numero(self):
        return "%s-%s" % (
            self.nosso_numero,
            self._dv_nosso_numero()
        )

    def _dv_nosso_numero(self):
        return str(self.modulo11(self.nosso_numero, 9, 0))

    @property
    def campo_livre(self):
        content = "".join([
                           '9',
                           self.conta_cedente,
                           self.nosso_numero,
                           self._dv_nosso_numero(),
                           self.ios,
                           self.carteira,
                           ])
        return content


class SantanderBoletoFields(BoletoFields):
    RECIDO_SACADO = 'Recibo do Pagador'
    SACADO = 'Pagador'
    CEDENTE = 'Beneficiário'
    AG_COD_CEDENTE = 'Agência/ Código Beneficiário'


class BoletoRegistradoSantander(BoletoSantander):
    '''
        Create necessary data for registered boleto on Santander
    '''

    def __init__(self, **kwargs):
        super(BoletoRegistradoSantander, self).__init__(**kwargs)

        self.carteira = '101'
        self.fields = SantanderBoletoFields

    @property
    def nosso_numero_by_santander(self):
        """ On new Webservice for boleto,
            santander can create their own
            nosso_numero with 13 digits
            and without dv
        """
        return len(self.nosso_numero) == 13

    def format_nosso_numero(self):
        if self.nosso_numero_by_santander:
            return self.nosso_numero

        return super(BoletoRegistradoSantander, self).format_nosso_numero()

    def _dv_nosso_numero(self):
        if self.nosso_numero_by_santander:
            return ''

        return super(BoletoRegistradoSantander, self)._dv_nosso_numero()

    @property
    def linha_digitavel(self):
        if self.code_line:
            return self.code_line

        return super(BoletoRegistradoSantander, self).linha_digitavel

    @property
    def barcode(self):
        if self.codigo_barras:
            return self.codigo_barras

        return super(BoletoSantander, self).barcode
