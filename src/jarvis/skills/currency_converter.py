"""Currency converter skill — convert between currencies using exchange rates."""

import re
import requests
from .registry import Skill, SkillResult

# Common currency codes
CURRENCIES = {
    "usd", "eur", "gbp", "jpy", "aud", "cad", "chf", "cny", "inr",
    "krw", "mxn", "brl", "rub", "sgd", "nzd", "hkd", "sek", "nok",
    "dkk", "pln", "thb", "try", "zar", "aed", "sar",
}


class CurrencyConverterSkill(Skill):
    name = "currency_converter"
    description = "Convert between currencies"
    triggers = ["currency", "exchange rate", "convert currency", "how much is", "convert usd", "convert eur"]

    _rates_cache = None
    _cache_time = None

    def matches(self, query: str) -> bool:
        """Check if this skill should handle the given query."""
        lower = query.lower().strip()
        # Check trigger phrases first
        for trigger in self.triggers:
            if trigger in lower:
                return True
        # Also check for currency codes in the query
        words = set(re.findall(r'\b[a-z]{3}\b', lower))
        return bool(words & CURRENCIES)

    def execute(self, query: str, context: dict) -> SkillResult:
        amount, from_currency, to_currency = self._parse_query(query)

        if amount is None or not from_currency or not to_currency:
            return SkillResult(
                success=False,
                message="Try a format like 'convert 100 USD to EUR' or 'how much is 50 euros in dollars'."
            )

        rates = self._get_rates()
        if not rates:
            return SkillResult(success=False, message="I couldn't fetch current exchange rates.")

        from_currency = from_currency.upper()
        to_currency = to_currency.upper()

        if from_currency not in rates or to_currency not in rates:
            known = ", ".join(sorted(rates.keys()))
            return SkillResult(
                success=False,
                message=f"I support these currencies: {known}."
            )

        # Convert: amount in from_currency -> USD -> to_currency
        usd_amount = amount / rates[from_currency]
        result = usd_amount * rates[to_currency]

        return SkillResult(
            success=True,
            message=f"{amount} {from_currency} is approximately {result:.2f} {to_currency}.",
            data={"from": from_currency, "to": to_currency, "amount": amount, "result": result}
        )

    def _parse_query(self, query: str) -> tuple:
        """Parse currency conversion queries."""
        import re
        lower = query.lower().strip()

        # Remove trigger words
        for trigger in self.triggers:
            if lower.startswith(trigger):
                lower = lower[len(trigger):].strip()

        # Pattern: <amount> <currency> to <currency>
        match = re.search(r'(\d+\.?\d*)\s*(\w{3})\s+to\s+(\w{3})', lower)
        if match:
            return float(match.group(1)), match.group(2), match.group(3)

        # Pattern: <amount> <currency_name> in <currency_name>
        match = re.search(r'(\d+\.?\d*)\s*(\w+)\s+in\s+(\w+)', lower)
        if match:
            amount = float(match.group(1))
            from_curr = self._normalize_currency(match.group(2))
            to_curr = self._normalize_currency(match.group(3))
            return amount, from_curr, to_curr

        return None, None, None

    def _normalize_currency(self, name: str) -> str:
        """Convert currency names to codes."""
        name_map = {
            "dollar": "usd", "dollars": "usd", "buck": "usd", "bucks": "usd",
            "euro": "eur", "euros": "eur",
            "pound": "gbp", "pounds": "gbp", "quid": "gbp",
            "yen": "jpy",
            "rupee": "inr", "rupees": "inr",
            "yuan": "cny",
            "won": "krw",
            "peso": "mxn", "pesos": "mxn",
            "franc": "chf", "francs": "chf",
            "krona": "sek", "kronor": "sek",
        }
        return name_map.get(name.lower(), name.lower())

    def _get_rates(self) -> dict | None:
        """Fetch current exchange rates (cached for 1 hour)."""
        import time

        now = time.time()
        if self._rates_cache and self._cache_time and (now - self._cache_time) < 3600:
            return self._rates_cache

        try:
            response = requests.get(
                "https://open.er-api.com/v6/latest/USD",
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            rates = data.get("rates", {})
            if rates:
                self._rates_cache = rates
                self._cache_time = now
                return rates
        except Exception:
            pass
        return None
