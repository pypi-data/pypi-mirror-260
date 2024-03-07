import pandas as pd, time, os, logging, sys
from pathlib import Path
#sys.path.append(str(Path(__file__).resolve().parent.parent))
from caluxPy_fi.FixedIncome import FixedIncome

class Multiple:

    def __init__(self, data, lang = 'eng'):

        logFormatter = logging.Formatter("%(asctime)s: [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
        _logger = logging.getLogger()
        _logger.setLevel(logging.DEBUG)
        fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), 'cMult'), mode = 'w', encoding = 'utf-8')
        fileHandler.setFormatter(logFormatter)
        _logger.addHandler(fileHandler)
    
        self.start_time = time.perf_counter()
        self.data = data
        self.mResults = []
        i = 0
        while i < len(data):
            for key, values in data[i].items():
                setattr(self, key[2:], values)
            
            settlement_date = self.settlementDate if lang == 'eng' else self.fechaLiquidacion if lang == 'esp' else ''
            issuance_date = self.issuanceDate if lang == 'eng' else self.fechaEmision if lang == 'esp' else ''
            maturity_date = self.maturityDate if lang == 'eng' else self.fechaVencimiento if lang == 'esp' else ''
            coupon = self.coupon if lang == 'eng' else self.cupon if lang == 'esp' else ''
            ytm = self.ytm if lang == 'eng' else self.rendimiento if lang == 'esp' else ''
            facial_value = self.facialValue if lang == 'eng' else self.monto if lang == 'esp' else ''
            issuer = self.issuer if lang == 'eng' else self.emisor if lang == 'esp' else ''
            methodology = self.methodology if lang == 'eng' else self.metodologia if lang == 'esp' else ''
            periodicity = self.periodicity if lang == 'eng' else self.periodicidad if lang == 'esp' else ''
            payment_type = self.paymentType if lang == 'eng' else self.tipoPago if lang == 'esp' else ''
            coupon_type = self.couponType if lang == 'eng' else self.tipoCupones if lang == 'esp' else ''
            forward_date = self.forwardDate if lang == 'eng' else self.forwardDate if lang == 'esp' else ''
            amortization_start_date = self.amotizationDate if lang == 'eng' else self.fechaAmortizacion if lang == 'esp' else ''
            amortization_periods = self.amortizationTimes if lang == 'eng' else self.cantidadAmortizaciones if lang == 'esp' else ''
            amortization_periodicity = self.amortizationPeriodicity if lang == 'eng' else self.periodicidadAmortizaciones if lang == 'esp' else ''
            amortizable_percentage = self.amortizablePercentage if lang == 'eng' else self.porcentajeAmortizable if lang == 'esp' else ''
            
            try:
                repos_margin = self.margin if lang == 'eng' else self.margen if lang == 'esp' else ''
            except Exception:
                repos_margin = None
            try:
                repo_rate = self.interestRate if lang == 'eng' else self.tasaInteres if lang == 'esp' else ''
            except Exception:
                repo_rate = None
            try:
                repo_tenure = self.repoTenure if lang == 'eng' else self.plazoRepos if lang == 'esp' else ''
            except Exception:
                repo_tenure = None

            calculador_results = FixedIncome(settlement_date = settlement_date, 
                                             issuance_date = issuance_date, 
                                             maturity_date = maturity_date, 
                                             coupon = coupon, 
                                             ytm = ytm, 
                                             face_value = facial_value, 
                                             issuer = issuer, 
                                             methodology = methodology, 
                                             periodicity = periodicity, 
                                             payment_type = payment_type, 
                                             coupon_type = coupon_type, 
                                             forward_date = forward_date, 
                                             amortization_start_date = amortization_start_date, 
                                             amortization_periods = amortization_periods, 
                                             amortization_periodicity = amortization_periodicity, 
                                             amortizable_percentage = amortizable_percentage, 
                                             date_format = '%Y-%m-%d', 
                                             multiple = True,
                                             repo_margin = repos_margin,
                                             repo_rate = repo_rate,
                                             repo_tenure = repo_tenure,
                                             lang = lang).get_results()

            self.mResults.append(calculador_results)
            if lang == 'eng':
                _logger.info(f'Calculated - {i + 1} of {len(data)}')
            elif lang == 'esp':
                _logger.info(f'Calculados - {i + 1} de {len(data)}')
            i += 1

        self.df_resultados_multiples = pd.DataFrame(self.mResults)
        self.end_time = time.perf_counter()
        self.process_time = self.end_time - self.start_time
        if lang == 'eng':
            _logger.info(f'{self.process_time} segs')
        elif lang == 'esp':
            _logger.info(f'{self.process_time} secs')
        _logger.removeHandler(fileHandler)
        fileHandler.close()

    def get_results(self):

        return self.mResults

    def get_results_df(self):

        return self.df_resultados_multiples
    
    def processTime(self):

        return self.process_time