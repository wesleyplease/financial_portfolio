import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

##  Strategy pattern - allows us to define a family of algorithms (valuation methods) and make them interchangeable.

# Define valuation strategies
class ValuationStrategy(ABC):
    @abstractmethod
    def calculate(self, fundamentals):
        pass

class DCFValuation(ValuationStrategy):
    def calculate(self, fundamentals):
        cash_flows = fundamentals['cash_flows']
        discount_rate = fundamentals['discount_rate']
        pv = sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows, start=1))
        return pv

class CompsValuation(ValuationStrategy):
    def calculate(self, fundamentals):
        target_metrics = fundamentals['target_metrics']
        peer_metrics = fundamentals['peer_metrics']
        avg_peer_metrics = {k: sum(v) / len(v) for k, v in peer_metrics.items()}
        valuation = {k: target_metrics[k] * avg_peer_metrics[k] for k in target_metrics}
        return valuation

class PrecedentTransactionsValuation(ValuationStrategy):
    def calculate(self, fundamentals):
        target_metrics = fundamentals['target_metrics']
        transactions_metrics = fundamentals['transactions_metrics']
        avg_transaction_metrics = {k: sum(v) / len(v) for k, v in transactions_metrics.items()}
        valuation = {k: target_metrics[k] * avg_transaction_metrics[k] for k in target_metrics}
        return valuation

class DDMValuation(ValuationStrategy):
    def calculate(self, fundamentals):
        dividends = fundamentals['dividends']
        discount_rate = fundamentals['discount_rate']
        pv = sum(d / (1 + discount_rate) ** i for i, d in enumerate(dividends, start=1))
        return pv

class BondValuation(ValuationStrategy):
    def calculate(self, fundamentals):
        cash_flows = fundamentals['bond_cash_flows']
        discount_rate = fundamentals['discount_rate']
        pv = sum(cf / (1 + discount_rate) ** i for i, cf in enumerate(cash_flows, start=1))
        return pv

class YTMValuation(ValuationStrategy):
    def calculate(self, fundamentals):
        current_price = fundamentals['current_price']
        coupon_rate = fundamentals['coupon_rate']
        face_value = fundamentals['face_value']
        years_to_maturity = fundamentals['years_to_maturity']
        
        def ytm_function(rate):
            return sum((coupon_rate * face_value) / (1 + rate) ** t for t in range(1, years_to_maturity + 1)) + face_value / (1 + rate) ** years_to_maturity - current_price

        low, high = 0, 1
        while ytm_function(high) > 0:
            low, high = high, high * 2
        while high - low > 1e-6:
            mid = (low + high) / 2
            if ytm_function(mid) > 0:
                low = mid
            else:
                high = mid
        return high

class ValuationContext:
    def __init__(self, strategy: ValuationStrategy):
        self.strategy = strategy

    def execute_strategy(self, fundamentals):
        return self.strategy.calculate(fundamentals)

# GUI Implementation
class ValuationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Valuationator")
        self.root.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both")

        self.create_dcf_tab()
        self.create_comps_tab()
        self.create_precedent_tab()
        self.create_ddm_tab()
        self.create_bond_tab()
        self.create_ytm_tab()

    def create_dcf_tab(self):
        self.dcf_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.dcf_tab, text="DCF Valuation")

        ttk.Label(self.dcf_tab, text="Cash Flows (comma-separated)").pack(pady=10)
        self.dcf_cash_flows = ttk.Entry(self.dcf_tab)
        self.dcf_cash_flows.pack(pady=5)

        ttk.Label(self.dcf_tab, text="Discount Rate").pack(pady=10)
        self.dcf_discount_rate = ttk.Entry(self.dcf_tab)
        self.dcf_discount_rate.pack(pady=5)

        self.dcf_result = ttk.Label(self.dcf_tab, text="")
        self.dcf_result.pack(pady=20)

        self.dcf_button = ttk.Button(self.dcf_tab, text="Calculate", command=self.calculate_dcf)
        self.dcf_button.pack(pady=10)

    def create_comps_tab(self):
        self.comps_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.comps_tab, text="Comps Valuation")

        ttk.Label(self.comps_tab, text="Target Metrics (format: metric:value)").pack(pady=10)
        self.comps_target_metrics = ttk.Entry(self.comps_tab)
        self.comps_target_metrics.pack(pady=5)

        ttk.Label(self.comps_tab, text="Peer Metrics (format: metric:value1,value2...)").pack(pady=10)
        self.comps_peer_metrics = ttk.Entry(self.comps_tab)
        self.comps_peer_metrics.pack(pady=5)

        self.comps_result = ttk.Label(self.comps_tab, text="")
        self.comps_result.pack(pady=20)

        self.comps_button = ttk.Button(self.comps_tab, text="Calculate", command=self.calculate_comps)
        self.comps_button.pack(pady=10)

    def create_precedent_tab(self):
        self.precedent_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.precedent_tab, text="Precedent Transactions")

        ttk.Label(self.precedent_tab, text="Target Metrics (format: metric:value)").pack(pady=10)
        self.precedent_target_metrics = ttk.Entry(self.precedent_tab)
        self.precedent_target_metrics.pack(pady=5)

        ttk.Label(self.precedent_tab, text="Transactions Metrics (format: metric:value1,value2...)").pack(pady=10)
        self.precedent_transactions_metrics = ttk.Entry(self.precedent_tab)
        self.precedent_transactions_metrics.pack(pady=5)

        self.precedent_result = ttk.Label(self.precedent_tab, text="")
        self.precedent_result.pack(pady=20)

        self.precedent_button = ttk.Button(self.precedent_tab, text="Calculate", command=self.calculate_precedent)
        self.precedent_button.pack(pady=10)

    def create_ddm_tab(self):
        self.ddm_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.ddm_tab, text="DDM Valuation")

        ttk.Label(self.ddm_tab, text="Dividends (comma-separated)").pack(pady=10)
        self.ddm_dividends = ttk.Entry(self.ddm_tab)
        self.ddm_dividends.pack(pady=5)

        ttk.Label(self.ddm_tab, text="Discount Rate").pack(pady=10)
        self.ddm_discount_rate = ttk.Entry(self.ddm_tab)
        self.ddm_discount_rate.pack(pady=5)

        self.ddm_result = ttk.Label(self.ddm_tab, text="")
        self.ddm_result.pack(pady=20)

        self.ddm_button = ttk.Button(self.ddm_tab, text="Calculate", command=self.calculate_ddm)
        self.ddm_button.pack(pady=10)

    def create_bond_tab(self):
        self.bond_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.bond_tab, text="Bond Valuation")

        ttk.Label(self.bond_tab, text="Bond Cash Flows (comma-separated)").pack(pady=10)
        self.bond_cash_flows = ttk.Entry(self.bond_tab)
        self.bond_cash_flows.pack(pady=5)

        ttk.Label(self.bond_tab, text="Discount Rate").pack(pady=10)
        self.bond_discount_rate = ttk.Entry(self.bond_tab)
        self.bond_discount_rate.pack(pady=5)

        self.bond_result = ttk.Label(self.bond_tab, text="")
        self.bond_result.pack(pady=20)

        self.bond_button = ttk.Button(self.bond_tab, text="Calculate", command=self.calculate_bond)
        self.bond_button.pack(pady=10)

    def create_ytm_tab(self):
        self.ytm_tab = ttk.Frame(self.tabs)
        self.tabs.add(self.ytm_tab, text="YTM Valuation")

        ttk.Label(self.ytm_tab, text="Current Price").pack(pady=10)
        self.ytm_current_price = ttk.Entry(self.ytm_tab)
        self.ytm_current_price.pack(pady=5)

        ttk.Label(self.ytm_tab, text="Coupon Rate").pack(pady=10)
        self.ytm_coupon_rate = ttk.Entry(self.ytm_tab)
        self.ytm_coupon_rate.pack(pady=5)

        ttk.Label(self.ytm_tab, text="Face Value").pack(pady=10)
        self.ytm_face_value = ttk.Entry(self.ytm_tab)
        self.ytm_face_value.pack(pady=5)

        ttk.Label(self.ytm_tab, text="Years to Maturity").pack(pady=10)
        self.ytm_years_to_maturity = ttk.Entry(self.ytm_tab)
        self.ytm_years_to_maturity.pack(pady=5)

        self.ytm_result = ttk.Label(self.ytm_tab, text="")
        self.ytm_result.pack(pady=20)

        self.ytm_button = ttk.Button(self.ytm_tab, text="Calculate", command=self.calculate_ytm)
        self.ytm_button.pack(pady=10)

    def calculate_dcf(self):
        cash_flows = list(map(float, self.dcf_cash_flows.get().split(',')))
        discount_rate = float(self.dcf_discount_rate.get())
        context = ValuationContext(DCFValuation())
        result = context.execute_strategy({'cash_flows': cash_flows, 'discount_rate': discount_rate})
        self.dcf_result.config(text=f"DCF Valuation: {result:.2f}")

    def calculate_comps(self):
        target_metrics = dict(item.split(':') for item in self.comps_target_metrics.get().split(','))
        target_metrics = {k: float(v) for k, v in target_metrics.items()}
        peer_metrics = dict(item.split(':') for item in self.comps_peer_metrics.get().split(','))
        peer_metrics = {k: list(map(float, v.split(','))) for k, v in peer_metrics.items()}
        context = ValuationContext(CompsValuation())
        result = context.execute_strategy({'target_metrics': target_metrics, 'peer_metrics': peer_metrics})
        self.comps_result.config(text=f"Comps Valuation: {result}")

    def calculate_precedent(self):
        target_metrics = dict(item.split(':') for item in self.precedent_target_metrics.get().split(','))
        target_metrics = {k: float(v) for k, v in target_metrics.items()}
        transactions_metrics = dict(item.split(':') for item in self.precedent_transactions_metrics.get().split(','))
        transactions_metrics = {k: list(map(float, v.split(','))) for k, v in transactions_metrics.items()}
        context = ValuationContext(PrecedentTransactionsValuation())
        result = context.execute_strategy({'target_metrics': target_metrics, 'transactions_metrics': transactions_metrics})
        self.precedent_result.config(text=f"Precedent Transactions Valuation: {result}")

    def calculate_ddm(self):
        dividends = list(map(float, self.ddm_dividends.get().split(',')))
        discount_rate = float(self.ddm_discount_rate.get())
        context = ValuationContext(DDMValuation())
        result = context.execute_strategy({'dividends': dividends, 'discount_rate': discount_rate})
        self.ddm_result.config(text=f"DDM Valuation: {result:.2f}")

    def calculate_bond(self):
        cash_flows = list(map(float, self.bond_cash_flows.get().split(',')))
        discount_rate = float(self.bond_discount_rate.get())
        context = ValuationContext(BondValuation())
        result = context.execute_strategy({'bond_cash_flows': cash_flows, 'discount_rate': discount_rate})
        self.bond_result.config(text=f"Bond Valuation: {result:.2f}")

    def calculate_ytm(self):
        current_price = float(self.ytm_current_price.get())
        coupon_rate = float(self.ytm_coupon_rate.get())
        face_value = float(self.ytm_face_value.get())
        years_to_maturity = int(self.ytm_years_to_maturity.get())
        context = ValuationContext(YTMValuation())
        result = context.execute_strategy({
            'current_price': current_price,
            'coupon_rate': coupon_rate,
            'face_value': face_value,
            'years_to_maturity': years_to_maturity
        })
        self.ytm_result.config(text=f"YTM: {result:.4f}")

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ValuationApp(root)
    root.mainloop()
