class Purchases:
    def __init__(self) -> None:
        self.purchases = []
        
    def get_purchases(self) -> str:
        text = '\n\t\t'.join(self.purchases)
        text = (
            f'Список покупок:\n\t\t'
            f'{text}'
        )
        return text

    def normalize_purchases(self, purchases: list) -> list:
        normalized_purchases = list(
            map(
                lambda purchase: purchase.lower(),
                purchases,
            )
        )
        return normalized_purchases

    def add_purchases(self, new_purchases: list) -> None:
        norm_purchases = self.normalize_purchases(new_purchases)
        self.purchases = [
            *self.purchases,
            *norm_purchases,
        ]

    def remove_purchases(self, purchases: list) -> None:
        norm_purchases = self.normalize_purchases(purchases)
        for purchase in norm_purchases:
            self.purchases.remove(purchase)

    def check_action(self, text: str) -> None:
        if text == '':
            return
        if text.startswith(('+', '-')):
            action = text[0]
            items = text[1:].split(' ')
            if action == '+':
                self.add_purchases(items)
            if action == '-':
                self.remove_purchases(items)

    def clean_purchases(self) -> None:
        self.purchases = []